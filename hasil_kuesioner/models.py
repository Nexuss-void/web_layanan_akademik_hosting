from django.db import models

class HasilKuesioner(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question = models.ForeignKey('question.Question', on_delete=models.CASCADE)
    emotion = models.CharField(max_length=20)
    emotion_details=models.JSONField()
    image = models.ImageField(upload_to='data gambar wajah/', null=True, blank=True)
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hasil Kuesioner - User: {self.user.email}, Question: {self.question.question_text}, Emotion: {self.emotion}"