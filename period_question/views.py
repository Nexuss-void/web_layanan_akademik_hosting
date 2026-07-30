from django.shortcuts import render
from users.views import is_admin
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from period_question.models import PeriodQuestion
from question.models import Question
from django.core.paginator import Paginator


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
        return redirect('list_periods')
    
    return render(
        request, 
        'crud_data/create_period.html',)

@user_passes_test(is_admin)
def create_question(request):
    periods=PeriodQuestion.objects.all()
    if request.method == 'POST':   
        Question.objects.create(
            period_id=request.POST.get('period'),
            question_text=request.POST.get('question_text'),
            order_number=request.POST.get('order_number'),
            category=request.POST.get('category')
        )
        messages.success(request,'Pertanyaan berhasil ditambahkan')
        return redirect('list_questions')
    
    return render(
        request, 
        'crud_data/create_question.html',
        {
            'periods':periods
            })

@user_passes_test(is_admin)
def list_periods(request):
    status_filter=request.GET.get('status')
    semester_filter=request.GET.get('semester')
    periods=PeriodQuestion.objects.all().order_by('-id')

    if status_filter:
        periods=periods.filter(status=status_filter)
    if semester_filter:
        periods=periods.filter(semester=semester_filter)

    paginator = Paginator(periods,10)
    page_number = request.GET.get('page')
    periods = paginator.get_page(page_number ) 
    return render(
        request,
        'crud_data/list_period.html',{
            "periods":periods,
            "selected_status":status_filter,
            "selected_semester":semester_filter
        }
    )

@user_passes_test(is_admin)
def list_questions(request):
    period_filter=request.GET.get('period')
    category_filter=request.GET.get('category')
    questions=Question.objects.select_related('period').all().order_by('-id')
    periods=PeriodQuestion.objects.filter(status='Aktif')
    categories=Question.objects.values_list('category', flat=True).distinct().order_by('category')

    if period_filter:
        questions=questions.filter(period_id=period_filter)
    if category_filter:
        questions=questions.filter(category=category_filter)

    paginator = Paginator(questions,10)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number )
    return render(
        request,
        'crud_data/list_question.html',{
            "questions":questions,
            "periods":periods,
            "categories":categories,
            "selected_period":period_filter,
            "selected_category":category_filter
        }
    )

@user_passes_test(is_admin)
def edit_period(request,pk):
    period= get_object_or_404(PeriodQuestion,id=pk)
    if request.method =='POST':
        period.semester = request.POST.get('semester')
        period.tahun_ajaran = request.POST.get('tahun_ajaran')
        period.status = request.POST.get('status')
        period.save()
        messages.success(request,'Periode berhasil diperbaharui')
        return redirect('list_periods')
    return render(
        request,
        'crud_data/create_period.html',{
            'period':period
        }
    )

@user_passes_test(is_admin)
def edit_question(request,pk):
    question= get_object_or_404(Question,id=pk)
    periods=PeriodQuestion.objects.all()
    if request.method =='POST':
        question.period_id = request.POST.get('period')
        question.question_text = request.POST.get('question_text')
        question.order_number = request.POST.get('order_number')
        question.category = request.POST.get('category')
        question.save()
        messages.success(request,'Pertanyaan berhasil diperbaharui')
        return redirect('list_questions')
    return render(
        request,
        'crud_data/create_question.html',{
            'question':question,
            'periods':periods
        }
    )    