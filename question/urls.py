from django.urls import path
from . import views

urlpatterns = [
    path('<int:period_id>/<int:order_number>/', views.ui_kuesioner, name='ui_kuesioner'),
    path('kuesioner/<int:period_id>/', views.start_kuesioner, name='start_kuesioner'),
]