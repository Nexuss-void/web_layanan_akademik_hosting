from django.urls import path
from . import views
urlpatterns = [
    path('hapus-hasil/<str:session_id>/',views.hapus_hasil,name='hapus_hasil'),
    path('analysis/', views.analysis_view, name='analysis_view'),
]