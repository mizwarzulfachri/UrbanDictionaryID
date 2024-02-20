from django import forms
from django.contrib.auth.models import User

from .models import Report, Censorship
from word.models import Word

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'user',
            'word',
            'category',
            'description',
            'option',
        ]

class RawReportForm(forms.Form):
    Choice = [
        ("Vulgar", "Vulgar"),
        ("Spam", "Spam"),
    ]

    user        = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    word        = forms.ModelChoiceField(queryset=Word.objects.all(), widget=forms.HiddenInput)
    category    = forms.ChoiceField(
        choices=Choice,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
        }
    ))
    description = forms.CharField(
        widget = forms.Textarea(
            attrs={
                "placeholder": "Masukan keterangan",
                "rows": 10,
                "cols": 50,
            }
        )
    )

class CensorshipForm(forms.ModelForm):
    class Meta:
        model = Censorship
        fields = [
            'name',
            'description',
        ]

class RawCensorshipForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Masukkan Kata"}))
    description = forms.CharField(
        widget = forms.Textarea(
            attrs={
                "placeholder": "Masukan keterangan",
                "rows": 10,
                "cols": 50,
            }
        )
    )