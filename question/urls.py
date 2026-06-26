from django.urls import path
from . import views

urlpatterns = [
    path('<int:order_number>/', views.ui_kuesioner, name='ui_kuesioner'),
    path('start-kuesioner/', views.start_kuesioner, name='start_kuesioner'),
]