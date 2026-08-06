import uuid
from django.shortcuts import get_object_or_404, render, redirect
from period_question.models import PeriodQuestion
from hasil_kuesioner.models import HasilKuesioner
from users.views import is_user
from django.contrib.auth.decorators import user_passes_test

def start_kuesioner(request, period_id):
    period_obj=get_object_or_404(
        PeriodQuestion, 
        id=period_id
        )
    active_questions_ids=list(period_obj.questions.values_list('id',flat=True))
    existing_answers= HasilKuesioner.objects.filter(
        user=request.user,
        question__id__in=active_questions_ids
    )
    answered_count=existing_answers.count()
    if answered_count > 0:
        session_id=existing_answers.first().session_id
        current_step=answered_count
    else:
        session_id=str(uuid.uuid4())
        current_step=0

    request.session['kuesioner_session_id'] = session_id
    return redirect(
        'ui_kuesioner', 
        period_id=period_obj.id,
        step=current_step
        )

@user_passes_test(is_user)
def ui_kuesioner(request,period_id,step=0):
    period_obj=get_object_or_404(
        PeriodQuestion, 
        id= period_id
        )
    questions_list=list(period_obj.questions.all().order_by('id'))

    if step >= len(questions_list):
        return redirect('dashboard_user')
    questions=questions_list[step]
    next_step=step+1

    return render(request, 'question/ui_kuesioner.html', {
        'question': questions,
        'current_step': step,
        'next_step': next_step,
        'period_id': period_obj.id,
        'total_questions': len(questions_list)
        })