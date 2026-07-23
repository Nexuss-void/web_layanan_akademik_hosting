from django.urls import path
from . import views

urlpatterns = [
    path('<int:period>/<int:order_number>/', views.ui_kuesioner, name='ui_kuesioner'),
    path('<int:period>/', views.start_kuesioner, name='start_kuesioner'),
]