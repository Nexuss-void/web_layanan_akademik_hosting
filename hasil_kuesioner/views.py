from itertools import count

from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404, render,redirect
from users.views import is_admin
from django.contrib.auth.decorators import user_passes_test
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
    periods=PeriodQuestion.objects.filter(status="Aktif")
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