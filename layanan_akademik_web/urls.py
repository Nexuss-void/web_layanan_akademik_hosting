from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminonly/', admin.site.urls),
    path('', include('users.urls')),
    path('hasil-kuesioner/', include('hasil_kuesioner.urls')),
    path('profil-mahasiswa/', include('profil_mahasiswa.urls')),
    path('kuesioner/', include('question.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
