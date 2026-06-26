from django.shortcuts import render,redirect
from users.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from hasil_kuesioner.models import HasilKuesioner

@user_passes_test(is_admin)
def detail_hasil(request, session_id):
    hasil = HasilKuesioner.objects.filter(
        session_id=session_id
    ).order_by(
        'question__order_number'
    )
    user = hasil.first().user if hasil.exists() else None

    return render(
        request,
        'hasil_kuesioner/detail_hasil.html',
        {
            'hasil_list': hasil,
            'user_data': user
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

    return redirect('dashboard_admin')