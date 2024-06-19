from django.contrib import admin
from parler.admin import TranslatableAdmin

# Register your models here.
from .models import Report, Censorship

class ReportAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'word', 'description', 'date']
    search_fields = ['category', 'user', 'word']
    list_filter = ['category']
    list_per_page = 20

class CensorAdmin(TranslatableAdmin):
    list_display = ['name', 'date', 'description']
    search_fields = ['name', 'date']
    list_filter = ['name']
    list_per_page = 20

admin.site.register(Report, ReportAdmin)
admin.site.register(Censorship, CensorAdmin)