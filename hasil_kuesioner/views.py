from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404, render,redirect
from users.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from hasil_kuesioner.models import HasilKuesioner
from period_question.models import PeriodQuestion
from profil_mahasiswa.models import ProfilMahasiswa

@user_passes_test(is_admin)
def detail_hasil(request, user_id,period_id):
    profile = get_object_or_404(ProfilMahasiswa, user_id=user_id)
    period = get_object_or_404(PeriodQuestion, id=period_id)
    active_q_ids = list(period.questions.values_list('id', flat=True))
    hasil = HasilKuesioner.objects.filter(
        user_id=user_id,
        question__id__in=active_q_ids,
    ).select_related('question').order_by(
        'question__id'
    )
    return render(
        request,
        'hasil_kuesioner/detail_hasil.html',
        {
            'profile': profile,
            'period': period,
            'hasil_list': hasil
        }
    )

@user_passes_test(is_admin)
def hapus_hasil(request, session_id):
    hasil_list=HasilKuesioner.objects.filter(
        session_id=session_id
    )
    for hasil in hasil_list:
        if hasil.image:
            hasil.image.delete(save=False)
        hasil.delete()

    return redirect('list_mahasiswa')

@user_passes_test(is_admin)
def analysis_view(request):
    periods=PeriodQuestion.objects.filter(status="Aktif").order_by('id')
    selected_period_id = request.GET.get('period')
    selected_fakultas = request.GET.get('fakultas', 'FAST')
    fakultas_name = 'Fakultas Sains dan Teknologi' if selected_fakultas == 'FAST' else 'Fakultas Ekonomi dan Bisnis'

    if selected_period_id:
        selected_period=get_object_or_404(
            PeriodQuestion,
            id=selected_period_id,
            status='Aktif'
            )
    else:
        selected_period=periods.first()

    analysis={}
    if selected_period:
        total_question = selected_period.questions.count()
        completed_sessions = (
            HasilKuesioner.objects
            .filter(
                question__period_questions=selected_period
            )
            .values("session_id")
            .annotate(total_answer=Count("id"))
            .filter(total_answer=total_question)
            .values_list("session_id", flat=True)
        )
        categories=[
            "Akademik",
            "Non-Akademik",
            "Reputasi Universitas",
            "Aksesibilitas/Akses",
            "Isu Program Akademik",
            "Pemahaman Kebutuhan"
        ]
        for category in categories:
            result=HasilKuesioner.objects.filter(
                session_id__in=completed_sessions,
                question__in=selected_period.questions.filter(category=category),
                user__profilmahasiswa__fakultas=fakultas_name
            )
            count={
                "Sangat Puas": 0,
                "Puas": 0,
                "Tidak Puas": 0,
                "Sangat Tidak Puas": 0,
            }

            for item in result:
                satisfaction=item.emotion.split('|')[0].strip()
                if satisfaction in count:
                    count[satisfaction]+=1
            total=sum(count.values())
            if total>0:
                percentage={key:round(value/total *100,2) for key,value in count.items()}
                analysis[category]=percentage
            
    return render(request,'hasil_kuesioner/analysis.html',{
        "periods": periods,
        "selected_period": selected_period,
        "selected_fakultas": selected_fakultas,
        "analysis": analysis
    })

@user_passes_test(is_admin)
def list_hasil_kuesioner(request):
    status_filter=request.GET.get('status', '')
    search = request.GET.get('search', '')
    selected_period_id = request.GET.get('period', '')
    periods = PeriodQuestion.objects.all().order_by('-id')
    profiles=(ProfilMahasiswa.objects.select_related('user').all().order_by('nama'))

    if search:
        profiles = profiles.filter(
            Q(nama__icontains=search) |
            Q(nim__icontains=search)
        )

    if selected_period_id:
            selected_period=periods.filter(id=selected_period_id)
    else:
        selected_period=periods

    hasil_list=[]
    for profile in profiles:
        for period in selected_period:
            active_q_ids = list(
                    period.questions.values_list(
                        'id',
                        flat=True
                    )
                )
            
            total_question = len(active_q_ids)
            if total_question == 0:
                continue

            total_answer = (HasilKuesioner.objects
                        .filter(
                            user=profile.user,
                            question_id__in=active_q_ids
                        )
                        .values('question_id')
                        .distinct()
                        .count()
                    )
            if total_answer == 0:
                continue

            if total_answer >= total_question:
                status='Selesai'
            else:
                status='Belum Selesai'
            if status_filter and status != status_filter:
                continue
            hasil_list.append({
                'profile':profile,
                'period':period,
                'total_answer': total_answer,
                'total_question': total_question,
                'progres': f"Soal yang sudah dijawab: {total_answer} dari {total_question} soal",
                'status':status,
            })     

    paginator = Paginator(hasil_list,10)
    page_number = request.GET.get('page')
    hasil_list = paginator.get_page(page_number )   

    return render(
        request,
        'hasil_kuesioner/list_hasil_kuesioner.html',
        {
            'periods': periods,
            'selected_period_id': selected_period_id,
            'status_filter':status_filter,
            'search':search,
            'hasil_list': hasil_list,
            'hasil_list':hasil_list
        }
    )