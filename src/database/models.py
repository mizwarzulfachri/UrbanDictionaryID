from django.db import models
from django.contrib.auth.models import User

from word.models import Word

# Create your models here.

class Report(models.Model):
    Choice = [
        ("Vulgar", "Vulgar"),
        ("Spam", "Spam"),
    ]
    Options = [
        ("Selesai", "Selesai"),
        ("Tinjau", "Tinjau"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    category = models.CharField(max_length=8, choices=Choice)
    description = models.TextField(blank=False, null=False)
    date = models.DateField(auto_now=False, auto_now_add=True)

    option = models.CharField(max_length=8, choices=Options, default="Tinjau")

    class Meta:
        db_table='Report'

    def __str__(self):
        return self.category

class Censorship(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.TextField(blank=False, null=False)

    class Meta:
        db_table='Word Censorship'

    def __str__(self):
        return self.name