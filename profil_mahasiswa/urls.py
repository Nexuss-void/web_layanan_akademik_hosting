from django.urls import path
from . import views

urlpatterns = [
    path('profil-mahasiswa/', views.profil_mahasiswa_view, name='profil_mahasiswa'),
]