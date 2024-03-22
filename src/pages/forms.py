from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

# Check if email is unique
def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError(
            (f"{value} is taken."),
            params = {'value':value}
        )

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators = [validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']