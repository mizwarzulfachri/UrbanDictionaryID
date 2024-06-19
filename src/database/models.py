from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from word.models import Word

# Create your models here.

class Report(models.Model):
    Choice = [
        ("Vulgar", _("Vulgar")),
        ("Spam", _("Spam")),
    ]
    Options = [
        ("Selesai", _("Selesai")),
        ("Tinjau", _("Tinjau")),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    category = models.CharField(_('category'), max_length=8, choices=Choice)
    description = models.TextField(_('description'), blank=False, null=False)
    date = models.DateField(_('date'), auto_now=False, auto_now_add=True)

    option = models.CharField(_('option'), max_length=8, choices=Options, default="Tinjau")

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __str__(self):
        return self.category

class Censorship(TranslatableModel):
    name = models.CharField(_('name'), max_length=20)
    translations = TranslatedFields(
        description = models.TextField(_('description'), blank=False, null=False)
    )
    date = models.DateField(_('date'), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('censorship')
        verbose_name_plural = _('censorships')

    def __str__(self):
        return self.name