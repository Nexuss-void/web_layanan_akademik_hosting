from django.urls import path
from . import views
urlpatterns = [
    path('hapus-hasil/<str:session_id>/',views.hapus_hasil,name='hapus_hasil'),
    path('analysis/', views.analysis_view, name='analysis_view'),
    path('', views.list_hasil_kuesioner, name='list_hasil_kuesioner'),
    path('detail-hasil/<int:user_id>/<int:period_id>/', views.detail_hasil, name='detail_hasil'),
]