from django.urls import path
from . import views

urlpatterns = [
    path('create-period/', views.create_period, name='create_period'),
    path('create-question/', views.create_question, name='create_question'),
    path('list-period/', views.list_periods, name='list_periods'),
    path('list-question/', views.list_questions, name='list_questions'),
    path('edit-period/<int:pk>/', views.edit_period, name='edit_period'),
    path('edit-question/<int:pk>/', views.edit_question, name='edit_question'),
    path('manage-questions/<int:pk>/', views.manage_questions, name='manage_questions'),
]