from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from users.views import is_user
from profil_mahasiswa.models import ProfilMahasiswa

@user_passes_test(is_user)
def profil_mahasiswa_view(request):

    profil = ProfilMahasiswa.objects.filter(
        user=request.user
    ).first()

    if request.method == 'POST':

        nama = request.POST.get('nama', '').strip()
        nim = request.POST.get('nim', '').strip()
        jurusan = request.POST.get('jurusan', '').strip()
        alamat = request.POST.get('alamat', '').strip()
        nomor_hp = request.POST.get('nomor_hp', '').strip()

        # Validasi field wajib
        if not all([
            nama,
            nim,
            jurusan,
            alamat,
            nomor_hp
        ]):
            messages.error(
                request,
                'Semua field wajib diisi'
            )
            return redirect('profil_mahasiswa')

        # Validasi NIM unik
        nim_exist = ProfilMahasiswa.objects.filter(
            nim=nim
        ).exclude(
            user=request.user
        ).exists()

        if nim_exist:
            return render(
                request,
                'profil_mahasiswa/form_profile.html',
                {
                    'profil': profil,
                    'error_nim': 'NIM sudah terdaftar'
                }
            )
        
        if not nim.isdigit():
            return render(
                request,
                'profil_mahasiswa/form_profile.html',
                {
                    'profil': profil,
                    'error_nim': 'NIM hanya boleh angka'
                }
            )
        
        if not nomor_hp.isdigit():
            return render(
                request,
                'profil_mahasiswa/form_profile.html',
                {
                    'profil': profil,
                    'error_hp': 'Nomor HP hanya boleh angka'
                }
            )

        # Validasi Jurusan
        if jurusan == 'Ekonomi':
            fakultas = 'Fakultas Ekonomi dan Bisnis'
            semester = 2

        elif jurusan == 'Teknik Informatika':
            fakultas = 'Fakultas Sains danTeknik'
            semester = 6

        else:
            messages.error(
                request,
                'Jurusan tidak valid'
            )
            return redirect('profil_mahasiswa')

        if profil:

            profil.nama = nama
            profil.nim = nim
            profil.fakultas = fakultas
            profil.jurusan = jurusan
            profil.semester = semester
            profil.alamat = alamat
            profil.nomor_hp = nomor_hp

            profil.save()

            messages.success(
                request,
                'Profil berhasil diperbarui'
            )

        else:

            ProfilMahasiswa.objects.create(
                user=request.user,
                nama=nama,
                nim=nim,
                fakultas=fakultas,
                jurusan=jurusan,
                semester=semester,
                alamat=alamat,
                nomor_hp=nomor_hp
            )

            messages.success(
                request,
                'Profil berhasil disimpan'
            )

        return redirect('dashboard_user')

    return render(
        request,
        'profil_mahasiswa/form_profile.html',
        {
            'profil': profil
        }
    )
