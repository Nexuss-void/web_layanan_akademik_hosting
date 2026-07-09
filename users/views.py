from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.core.paginator import Paginator
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .service import opencv_service as opencv
from .service import fer_service as fer
from question.models import Question
from hasil_kuesioner.models import HasilKuesioner
from profil_mahasiswa.models import ProfilMahasiswa
from users.models import User
from django.core.files.base import ContentFile
import uuid
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='admin').exists():
                return redirect('dashboard_admin')
            
            if user.groups.filter(name='user').exists():
                if not ProfilMahasiswa.objects.filter(user=user).exists():
                    return redirect('profil_mahasiswa')
            return redirect('dashboard_user')
        else:
            messages.error(request, 'Email atau password salah')
            return redirect('login')
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'The password entered must be the same')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar')
            return redirect('register')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, '; '.join(e.messages))
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password)
        user_group,created = Group.objects.get_or_create(name='user')
        user.groups.add(user_group)
        messages.success(request, 'Registrasi berhasil. Silakan login.')
        return redirect('login')

    return render(request, 'users/register.html')
        
def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@user_passes_test(is_admin)
def admin_view(request):
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    session_list = (
        HasilKuesioner.objects
        .values(
            'session_id',
            'user__profilmahasiswa__nama',
            'user__email',
            # 'created_at'
        ).distinct()
    )
    
    data_hasil = []
    for item in session_list:

        jumlah_jawaban = HasilKuesioner.objects.filter(
            session_id=item['session_id']
        ).count()
        status = ( 'Selesai' if jumlah_jawaban >= 12 else 'Belum Selesai')

        data_hasil.append({
            'session_id': item['session_id'],
            'nama': item['user__profilmahasiswa__nama'],
            'email': item['user__email'],
            'jumlah_jawaban': jumlah_jawaban,
            'status': status,
            # 'created_at': item['created_at']
        })

    # Search
    if search:
        data_hasil = [
            item
            for item in data_hasil
            if search.lower() in item['nama'].lower()
            or search.lower() in item['email'].lower()
        ]

    # Filter Status
    if status_filter:
        data_hasil = [
            item
            for item in data_hasil
            if item['status'] == status_filter
        ]
    paginator = Paginator(
        data_hasil,
        10
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(
        page_number
    )   

    return render(request,'users/dashboard_admin.html', 
        {
        'session_list': page_obj,
        'page_obj':page_obj,
        'is_selesai':
            status_filter == 'Selesai',

        'is_belum_selesai':
            status_filter == 'Belum Selesai',
        }
    )

def is_user(user):
    return user.groups.filter(name='user').exists()

@user_passes_test(is_user)
def user_view(request):
    profil = ProfilMahasiswa.objects.filter(user=request.user).first()
    if not profil:
        return redirect('profil_mahasiswa')
    jumlah_jawaban = HasilKuesioner.objects.filter(
        user=request.user
    ).count()

    total_pertanyaan=12
    if jumlah_jawaban == 0:
        status_kuesioner = 'Belum Diisi'
    else:
        status_kuesioner = 'Selesai'

    return render(request, 'users/dashboard_user.html',
        {
            'user': request.user,
            'profil': profil,
            'status_kuesioner': status_kuesioner,
            'jumlah_jawaban': jumlah_jawaban,
            'sudah_selesai': jumlah_jawaban >= total_pertanyaan
        }
    )

@csrf_exempt
@user_passes_test(is_user)
def capture_image(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        })

    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        question_id = data.get('question_id')

        if not image_data:
            return JsonResponse({
                'success': False,
                'message': 'Gambar tidak ditemukan'
            })

        _, imgstr = image_data.split(';base64,')
        image_bytes = base64.b64decode(imgstr)
        result_detect_face = opencv.detect_face(image_bytes)

        if isinstance(result_detect_face, str):
            if result_detect_face == 'No face':
                return JsonResponse({
                    'success': False,
                    'message': 'Wajah tidak terdeteksi'
                })

            if result_detect_face == 'Multiple faces':
                return JsonResponse({
                    'success': False,
                    'message': 'Wajah terdeteksi lebih dari satu'
                })
            
        emotion_results = fer.detect_emotion(result_detect_face['fer_img'])
        
        if isinstance(emotion_results, str):
            return JsonResponse({
                'success': False,
                'message': 'Wajah tidak terdeteksi,silahkan ulangi'
            })

        print(type(result_detect_face))
        print(result_detect_face)
        print("EMOTION RESULTS:", emotion_results)

        question = get_object_or_404(Question,id=question_id)
        HasilKuesioner.objects.create(
            user=request.user,
            question=question,
            emotion=f"{emotion_results['kepuasan']} | {emotion_results['dominan_emotion']}",
            emotion_details=emotion_results['emotion_details'],
            image=result_detect_face['save_img'],
            session_id=request.session.get('kuesioner_session_id')
        )
        next_question = Question.objects.filter(order_number=question.order_number + 1).first()
        if not next_question:
            request.session.pop('kuesioner_session_id',None)

        return JsonResponse({
            'success': True,
            'message': 'Hasil berhasil disimpan',
            'next_question': (next_question.order_number if next_question else None)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

