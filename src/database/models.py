from django.db import models
from django.contrib.auth.models import User

from word.models import Word

# Create your models here.

class Report(models.Model):
    ops1 = "Vulgar"
    ops2 = "Spam"

    Choice = [
        (ops1, "Vulgar"),
        (ops2, "Spam"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    category = models.CharField(max_length=8, choices=Choice)
    description = models.TextField(blank=False, null=False)
    date = models.DateField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table='Report'

    def __str__(self):
        return self.category