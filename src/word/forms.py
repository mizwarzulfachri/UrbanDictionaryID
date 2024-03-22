from django import forms
from django.contrib.auth.models import User

from .models import Word, Tag

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = [
            'word',
            # 'pronunciation',
            'definition',
            'tags',
        ]

class RawWordForm(forms.Form):
    word          = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Masukkan sebuah word/frasa"}))
    pronunciation = forms.FileField(
        widget=forms.HiddenInput(), 
        required=False,
        )
    definition    = forms.CharField(
        widget = forms.Textarea(
            attrs={
                "placeholder": "Masukkan definisi",
                "rows": 10,
                'cols': 40,
                }
            )
        )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'name',
        ]

class RawTagForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Masukkan tag"}))