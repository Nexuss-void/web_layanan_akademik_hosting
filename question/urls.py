from django.urls import path
from . import views

urlpatterns = [
    path('<int:period_id>/', views.ui_kuesioner, name='ui_kuesioner'),
    path('<int:period_id>/<int:step>/', views.ui_kuesioner, name='ui_kuesioner'),
    path('start/<int:period_id>/', views.start_kuesioner, name='start_kuesioner'),
]