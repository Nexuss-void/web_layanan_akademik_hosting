from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard-admin/', views.admin_view, name='dashboard_admin'),
    path('dashboard-user/', views.user_view, name='dashboard_user'),
    path('capture/',views.capture_image,name='capture_image'),
    path('register/', views.register_view, name='register'),
]