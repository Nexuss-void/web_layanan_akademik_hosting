from django.shortcuts import render
from users.views import is_admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from period_question.models import PeriodQuestion
from question.models import Question

@user_passes_test(is_admin)
def create_period(request):
    if request.method == 'POST':
        semester = request.POST.get('semester')
        tahun_ajaran = request.POST.get('tahun_ajaran')
        status = request.POST.get('status')

        if PeriodQuestion.objects.filter(
            semester=semester,
            tahun_ajaran=tahun_ajaran,
        ).exists():
            messages.error(request, 'Periode sudah ada.')
            return redirect('create_period')

        PeriodQuestion.objects.create(
            semester=semester,
            tahun_ajaran=tahun_ajaran,
            status=status
        )
        messages.success(request,'Periode berhasil ditambahkan')
        return redirect('create_period')
    
    return render(
        request, 
        'create_data/create_period.html',)

@user_passes_test(is_admin)
def create_question(request):
    if request.method == 'POST':
        period_id = PeriodQuestion.objects.get(id=request.POST.get('period_id'))
        
        Question.objects.create(
            period_id=period_id,
            question_text=request.POST.get('question_text'),
            order_number=request.POST.get('order_number')
        )
        messages.success(request,'Pertanyaan berhasil ditambahkan')
        return redirect('create_question')
    
    return render(
        request, 
        'create_data/create_question.html',
        {
            'periods':PeriodQuestion.objects.all()
            })