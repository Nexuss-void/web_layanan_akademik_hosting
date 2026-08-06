from django.db import models

class Question(models.Model):
    question_text = models.TextField()

    CATEGORY = (
    ("Akademik","Akademik"),
    ("Non-Akademik","Non-Akademik"),
    ("Reputasi Universitas","Reputasi Universitas"),
    ("Aksesibilitas/Akses","Aksesibilitas/Akses"),
    ("Isu Program Akademik","Isu Program Akademik"),
    ("Pemahaman Kebutuhan","Pemahaman Kebutuhan"),
    )
    category = models.CharField(max_length=20, choices=CATEGORY,null=True, blank=True)

    def __str__(self):
        return self.question_text
    