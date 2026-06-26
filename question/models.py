from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    order_number = models.IntegerField()

    def __str__(self):
        return self.question_text
