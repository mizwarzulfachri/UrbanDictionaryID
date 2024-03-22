from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterUserForm
from django.contrib.auth.models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = RegisterUserForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)