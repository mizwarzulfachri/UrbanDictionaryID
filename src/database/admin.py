from django.contrib import admin

# Register your models here.
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'word', 'description', 'date']
    search_fields = ['category', 'user', 'word']
    list_filter = ['category']
    list_per_page = 20

admin.site.register(Report, ReportAdmin)