import uuid
from django.db.models import Q
from django.db.models.aggregates import Count
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
from period_question.models import PeriodQuestion
from users.models import User
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
            messages.error(request, 'Incorrect email or password.')
            return redirect('login')
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'The password entered must be the same.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'The email is already registered.Please use another email.')
            return redirect('register')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, '; '.join(e.messages))
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password)
        user_group,created = Group.objects.get_or_create(name='user')
        user.groups.add(user_group)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'users/register.html')
        
def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@user_passes_test(is_admin)
def admin_view(request):
    period_active=PeriodQuestion.objects.filter(status='Aktif').order_by('id').first()
    total_respondents=0
    positive_satisfaction_rate="0%"
    total_fast_users=0
    total_feb_users=0
    category_labels = [
            "Akademik",
            "Non-Akademik",
            "Reputasi Universitas",
            "Aksesibilitas/Akses",
            "Isu Program Akademik",
            "Pemahaman Kebutuhan"
        ]
    ordinal_labels = ['Sangat Puas', 'Puas', 'Tidak Puas', 'Sangat Tidak Puas']
    ordinal_data = [0, 0, 0, 0]
    data_fast = [0] * len(category_labels)
    data_feb = [0] * len(category_labels)

    if period_active:
        total_question = period_active.questions.count()
        completed_sessions = (
            HasilKuesioner.objects
            .filter(
                question__period_questions=period_active
            )
            .values("session_id")
            .annotate(total_answer=Count("id"))
            .filter(total_answer=total_question)
            .values_list("session_id", flat=True)
        )
        answers=HasilKuesioner.objects.filter(question__period_questions=period_active,session_id__in=completed_sessions)
        # Metric Card: Total Responden
        total_respondents=answers.values('user').distinct().count()

        # Group Bar Chart
        total_fast_users = answers.filter(
            user__profilmahasiswa__fakultas='Fakultas Sains dan Teknologi'
        ).values('user').distinct().count()

        total_feb_users = answers.filter(
            user__profilmahasiswa__fakultas='Fakultas Ekonomi dan Bisnis'
        ).values('user').distinct().count()

        dict_fast_positive = {categ: 0 for categ in category_labels}
        dict_fast_total = {categ: 0 for categ in category_labels}
        dict_feb_positive = {categ: 0 for categ in category_labels}
        dict_feb_total = {categ: 0 for categ in category_labels}

        raw_answers=answers.values('question__category','user__profilmahasiswa__fakultas','emotion')
        for item in raw_answers:
            categ = item['question__category']
            fakul = item['user__profilmahasiswa__fakultas']
            emo = str(item['emotion'] or '').strip().lower()
            if not emo or categ not in category_labels:
                continue

            is_positive = False
            if 'sangat tidak puas' in emo or 'tidak puas' in emo:
                is_positive = False
            elif 'sangat puas' in emo or 'puas' in emo:
                is_positive = True

            if fakul == 'Fakultas Sains dan Teknologi':
                dict_fast_total[categ] += 1
                if is_positive:
                    dict_fast_positive[categ] += 1
            elif fakul == 'Fakultas Ekonomi dan Bisnis':
                dict_feb_total[categ] += 1
                if is_positive:
                    dict_feb_positive[categ] += 1
        data_fast = [
            round((dict_fast_positive[cat] / dict_fast_total[cat]) * 100, 1) if dict_fast_total[cat] > 0 else 0
            for cat in category_labels
        ]
        data_feb = [
            round((dict_feb_positive[cat] / dict_feb_total[cat]) * 100, 1) if dict_feb_total[cat] > 0 else 0
            for cat in category_labels
        ]

        # Pie Chart
        ordinal_counter = {label: 0 for label in ordinal_labels}
        raw_emotions=answers.values_list('emotion',flat=True)

        for item in raw_emotions:
            if not item:
                continue
            emo = str(item).strip().lower()

            if 'sangat tidak puas' in emo:
                ordinal_counter['Sangat Tidak Puas'] += 1
            elif 'tidak puas' in emo:
                ordinal_counter['Tidak Puas'] += 1
            elif 'sangat puas' in emo:
                ordinal_counter['Sangat Puas'] += 1
            elif 'puas' in emo:
                ordinal_counter['Puas'] += 1
        ordinal_data=[ordinal_counter[label] for label in ordinal_labels]

        # Metric Card: Persentase Kepuasan Positif
        total_answers=sum(ordinal_counter.values())
        positive_answers=ordinal_counter.get('Sangat Puas',0) + ordinal_counter.get('Puas',0)
        if total_answers > 0:
            positive_satisfaction_rate = f"{round((positive_answers / total_answers) * 100, 1)}%"
        else:
            positive_satisfaction_rate = "0%"

    has_data=total_respondents > 0
    context={
        'period_active':period_active,
        'total_respondents':total_respondents,
        'positive_satisfaction_rate':positive_satisfaction_rate,
        'category_labels':category_labels,
        'data_fast':data_fast,
        'data_feb':data_feb,
        'total_fast_users': total_fast_users,
        'total_feb_users': total_feb_users,
        'emotion_labels':ordinal_labels,
        'emotion_data':ordinal_data,
        'has_data':has_data,
    }
    return render(request,'users/dashboard_admin.html',context)

def is_user(user):
    return user.groups.filter(name='user').exists()

@user_passes_test(is_user)
def user_view(request):
    profil = ProfilMahasiswa.objects.filter(user=request.user).first()
    if not profil:
        return redirect('profil_mahasiswa')
    
    periods=PeriodQuestion.objects.filter(status='Aktif').order_by('tahun_ajaran')
    selected_period_id = request.GET.get('period')

    if selected_period_id:
        selected_period=get_object_or_404(
            PeriodQuestion,
            id=selected_period_id,
            status='Aktif'
            )
    else:
        selected_period=periods.first()

    status_kuesioner = 'Belum Diisi'
    jumlah_jawaban = 0
    total_pertanyaan = 0
    sudah_selesai = False

    if selected_period:
        active_questions_ids=list(selected_period.questions.values_list('id',flat=True))
        total_pertanyaan=len(active_questions_ids)
        if total_pertanyaan > 0:
            jumlah_jawaban=HasilKuesioner.objects.filter(
                user=request.user,
                question__id__in=active_questions_ids
            ).values('question_id').distinct().count()

            if jumlah_jawaban == 0:
                status_kuesioner = 'Belum Diisi'
                sudah_selesai = False
            elif jumlah_jawaban >= total_pertanyaan:
                status_kuesioner = 'Selesai'
                sudah_selesai = True
            else:
                status_kuesioner = 'Belum Selesai'
                sudah_selesai = False
    else:
        status_kuesioner = 'Belum Diisi'
        jumlah_jawaban = 0
        sudah_selesai = False
    
    selected_period.total_pertanyaan = total_pertanyaan
    selected_period.jumlah_jawaban = jumlah_jawaban
    selected_period.status_kuesioner = status_kuesioner
    selected_period.sudah_selesai = sudah_selesai

    return render(request, 'users/dashboard_user.html',
        {
            'user': request.user,
            'profil': profil,
            'periods': periods,
            "selected_period": selected_period,
            "status_kuesioner": status_kuesioner,
            "jumlah_jawaban": jumlah_jawaban,
            "total_pertanyaan": total_pertanyaan,
            "sudah_selesai": sudah_selesai,
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

        session_id=request.session.get('kuesioner_session_id')
        if not session_id:
            existing=HasilKuesioner.first(user=request.user,question=question).first()
            session_id=existing.session_id if existing else str(uuid.uuid4())
        HasilKuesioner.objects.update_or_create(
            user=request.user,
            question=question,
            emotion=f"{emotion_results['kepuasan']} | {emotion_results['dominan_emotion']}",
            emotion_details=emotion_results['emotion_details'],
            image=result_detect_face['save_img'],
            session_id=session_id
        )
        current_step = int(data.get('current_step', 0))
        period_id=data.get('period_id')
        period= get_object_or_404(PeriodQuestion, id=period_id)
        total_questions=period.questions.count()
        next_step= current_step + 1

        if next_step >= total_questions:
            request.session.pop('kuesioner_session_id',None)
            is_completed = True
        else:
            is_completed = False

        return JsonResponse({
            'success': True,
            'message': 'Hasil berhasil disimpan',
            'period': period.id,
            'next_step': next_step,
            'is_completed': is_completed
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@user_passes_test(is_admin)
def list_mahasiswa(request):
    search = request.GET.get('search', '')
    profile_mahasiswa=ProfilMahasiswa.objects.select_related('user').all().order_by('nama')

    # Search
    if search:
        profile_mahasiswa=profile_mahasiswa.filter(
            Q(nama__icontains=search) |
            Q(nim__icontains=search) |
            Q(user__email__icontains=search)|
            Q(jurusan__icontains=search)|
            Q(fakultas__icontains=search)
        )

    paginator = Paginator(
        profile_mahasiswa,
        10
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(
        page_number
    )   

    return render(request,'profil_mahasiswa/list_mahasiswa.html', 
        {
        'search': search,
        'page_obj':page_obj,
        }
    )
