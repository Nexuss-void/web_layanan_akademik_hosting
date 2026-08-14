from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from period_question import views as period_views
from profil_mahasiswa import views as edit_profil_view

urlpatterns = [
    path('adminonly/', admin.site.urls),

    path('dashboard-admin/data-mahasiswa/', user_views.list_mahasiswa, name='list_mahasiswa'),
    path('dashboard-admin/data-mahasiswa/<int:user_id>', user_views.detail_mahasiswa, name='detail_mahasiswa'),
    path('dashboard-admin/data-mahasiswa/<int:user_id>/edit', edit_profil_view.edit_profil, name='edit_profil'),
    path('manage-questions/', period_views.manage_questions, name='manage_questions'),

    path('', include('users.urls')),
    path('hasil-kuesioner/', include('hasil_kuesioner.urls')),
    path('profil-mahasiswa/', include('profil_mahasiswa.urls')),
    path('kuesioner/', include('question.urls')),
    path('dashboard-admin/', include('period_question.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
