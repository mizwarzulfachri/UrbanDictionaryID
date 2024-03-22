from django.contrib import admin

# Models here.
from .models import Word, Tag, Pronounce

class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'date', 'up', 'down', 'pronunciation']
    search_fields = ['word', 'user', 'tags']
    list_filter = ['tags']
    list_per_page = 20

class PronounceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pronunciation']
    search_fields = ['name']
    list_per_page = 20

admin.site.register(Word, WordAdmin)
admin.site.register(Tag)
admin.site.register(Pronounce)