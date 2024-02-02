from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Report

# App models
from word.models import Word, Tag

# Create your views here.
def database_pg(request, *args, **kwargs):
    user = get_user_model()
    userlist = user.objects.all()

    wordlist = Word.objects.all()
    taglist = Tag.objects.all()

    context = {
        "uobject": userlist,
        "wobject": wordlist,
        "tobject": taglist,
    }
    return render(request, "database/database.html", context)

def report_pg(request, srch_id):
    report = Report.objects.get(pk=srch_id)

    context = {
        'report': report,
    }
    return render(request, "database/report.html", context)

def form_rppg(request):
    form = RawReportForm