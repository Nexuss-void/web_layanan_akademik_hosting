from django.db import models

class ProfilMahasiswa(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=12, unique=True)
    jurusan = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    semester=models.IntegerField()
    alamat = models.TextField()
    nomor_hp = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nama} ({self.nim})"
    

