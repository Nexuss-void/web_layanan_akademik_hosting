from django.urls import path
from . import views
urlpatterns = [
    path('detail-hasil/<str:session_id>/', views.detail_hasil, name='detail_hasil'),
    path('hapus-hasil/<str:session_id>/',views.hapus_hasil,name='hapus_hasil'),
]