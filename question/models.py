from django.db import models

class Question(models.Model):
    period=models.ForeignKey('period_question.PeriodQuestion', on_delete=models.CASCADE,null=True, blank=True)
    question_text = models.TextField()
    order_number = models.IntegerField()

    CATEGORY = (
    ("Academic","Academic"),
    ("Non-Academic","Non-Academic"),
    ("Reputation","Reputation"),
    ("Access","Access"),
    ("Program Issues","Program Issues"),
    ("Understanding","Understanding"),
    )
    category = models.CharField(max_length=20, choices=CATEGORY,null=True, blank=True)

    def __str__(self):
        return self.question_text
