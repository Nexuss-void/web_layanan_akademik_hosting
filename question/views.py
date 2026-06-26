import uuid
from django.shortcuts import get_object_or_404, render, redirect
from users.views import is_user
from django.contrib.auth.decorators import user_passes_test
from question.models import Question

def start_kuesioner(request):
    request.session['kuesioner_session_id'] = str(uuid.uuid4())
    print("START_KUESIONER DIPANGGIL")
    return redirect('ui_kuesioner',order_number=1)

@user_passes_test(is_user)
def ui_kuesioner(request,order_number):
    questions = get_object_or_404(Question, order_number=order_number)
    next_question = Question.objects.filter(order_number=order_number + 1).first()
    return render(request, 'question/ui_kuesioner.html', {
        'question': questions, 
        'next_question': next_question
        })