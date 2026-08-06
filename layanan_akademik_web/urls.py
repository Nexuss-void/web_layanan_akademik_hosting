from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from period_question import views as period_views
from hasil_kuesioner import views as hasil_views

urlpatterns = [
    path('adminonly/', admin.site.urls),

    path('dashboard-admin/data-mahasiswa/', user_views.list_mahasiswa, name='list_mahasiswa'),
    path('dashboard-admin/data-mahasiswa/periode/<int:user_id>/', period_views.list_periods_mahasiswa, name='list_periods_mahasiswa'),
    path('dashboard-admin/data-mahasiswa/detail-hasil/<int:user_id>/<int:period_id>/', hasil_views.detail_hasil, name='detail_hasil'),

    path('', include('users.urls')),
    path('hasil-kuesioner/', include('hasil_kuesioner.urls')),
    path('profil-mahasiswa/', include('profil_mahasiswa.urls')),
    path('kuesioner/', include('question.urls')),
    path('dashboard-admin/', include('period_question.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
