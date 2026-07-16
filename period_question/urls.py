from django.urls import path
from . import views

urlpatterns = [
    path('create-period/', views.create_period, name='create_period'),
    path('create-question/', views.create_question, name='create_question'),
]