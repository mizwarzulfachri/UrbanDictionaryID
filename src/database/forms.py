from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm

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
        ("Vulgar", _("Vulgar")),
        ("Spam", _("Spam")),
        ("Slur", _("Slur")),
        ("Other", _("Other")),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

class CensorshipForm(TranslatableModelForm):
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