from django.contrib import admin

# Models here.
from .models import Word, Tag, Pronounce
from parler.admin import TranslatableAdmin

class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'date', 'up', 'down', 'visibility']
    search_fields = ['word', 'user__username', 'tags__translations__name']
    list_filter = ['tags__translations__name']
    list_per_page = 20

class PronounceAdmin(admin.ModelAdmin):
    list_display = ['name', 'visibility']
    search_fields = ['name']
    list_per_page = 20

admin.site.register(Word, WordAdmin)
admin.site.register(Tag, TranslatableAdmin)
admin.site.register(Pronounce)