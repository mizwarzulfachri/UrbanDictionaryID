from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    # 1 to many relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Attributes of the model
    word = models.CharField(max_length=120)
    definition = models.TextField(blank=False, null=False)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # Tags for searching and label
    pronunciation = models.ForeignKey('Pronounce', blank=True, null=True, on_delete=models.PROTECT, related_name="word_pronunciation")
    tags = models.ManyToManyField('Tag', blank=True, related_name="word_tag")

    class Meta:
        db_table='Word'

    def __str__(self):
        return self.word

    @property
    def rating(self):
        if self.up == 0:
            rating = 0
        elif self.up == 0 and self.down == 0:
            rating = 0
        else:
            percentage = self.up / (self.up + self.down)
            rating = percentage * 100
        return rating

    @property
    def text2speech(self):
        return reverse('text_to_speech', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse("word:word", kwargs={"wrd_id": self.id}) # Dynamic ver.
        # f"/word/{self.id}/" # Hardcode ver.

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Upvotes(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="user_up")
    word = models.ForeignKey(Word, models.CASCADE, related_name="word_up")

class Downvotes(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="user_down")
    word = models.ForeignKey(Word, models.CASCADE, related_name="word_down")

class Pronounce(models.Model):
    name = models.CharField(max_length=120)
    pronunciation = models.FileField(blank=True, null=True, upload_to='pronunciation/')

    def __str__(self):
        return self.name