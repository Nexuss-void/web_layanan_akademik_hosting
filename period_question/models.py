from django.db import models

class PeriodQuestion(models.Model):
    semester = models.CharField(
        max_length=10,
        choices=[('Ganjil', 'Ganjil'), ('Genap', 'Genap')]
        )
    tahun_ajaran = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], 
        default='Aktif'
        )

    def __str__(self):
        return f"{self.semester} - {self.tahun_ajaran} - {self.status}"