from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

from .forms import ReportForm, RawReportForm, CensorshipForm, RawCensorshipForm

from .models import Report, Censorship

# App models
from word.models import Word, Tag

# Create your views here.
# Database homepage
def database_pg(request, *args, **kwargs):
    page = 'database'

    user = get_user_model()
    userlist = user.objects.all().order_by('-date_joined')

    wordlist = Word.objects.all().order_by('word')
    taglist = Tag.objects.all().order_by('name')
    reportlist = Report.objects.filter(Q(option__icontains="Tinjau"))
    countrpt = reportlist.count()

    # Search
    if request.GET.get('s') != None:
        q = request.GET.get('s')
        wordlist = Word.objects.filter(
            Q(word__istartswith=q) 
            ).order_by('word', '-up')

        userlist = set()
        for word in wordlist:
            userlist.add(word.user)

    if request.GET.get('t') != None: 
        q = request.GET.get('t')
        wordlist = Word.objects.filter(Q(tags__name__icontains=q)).order_by('word', '-up',)

        userlist = set()
        for word in wordlist:
            userlist.add(word.user)

    context = {
        "uobject": userlist,
        "wobject": wordlist,
        "tobject": taglist,
        "count": countrpt,
        "page": page,
    }
    return render(request, "database/database.html", context)

# Report List
def report_list(request):
    page = "list"
    reportlist = Report.objects.filter(Q(option__icontains="Tinjau")).order_by("date")
    donelist = Report.objects.filter(Q(option__icontains="Selesai")).order_by("date")
    censorlist = Censorship.objects.all().order_by('name')

    context = {
        "robject": reportlist,
        "done": donelist,
        "censored": censorlist,
        "page": page,
    }
    return render(request, "database/database.html", context)

# View Reports 
def report_view(request, srch_id):
    page = 'view'
    report = get_object_or_404(Report, pk=srch_id)

    context = {
        'report': report,
        'page': page,
    }
    return render(request, "database/report.html", context)

# Report Form
def form_rppg(request, pk):
    page = 'form'

    form = RawReportForm()
    word_object = get_object_or_404(Word, pk=pk)

    if request.method == "POST":
        form_data = {
            'word': word_object,
            'user': request.user,
            'category': request.POST.get('category'),
            'description': request.POST.get('description'),
        }

        form = RawReportForm(form_data)
        if form.is_valid():
            print(form.cleaned_data)
            Report.objects.create(**form.cleaned_data)
            return redirect('home')
        else:
            print(form.errors)

    context = {
        'form': form,
        'word': word_object,
        'page': page,
    }
    return render(request, "database/report_form.html", context)

def report_del(request, pk):
    page = 'delete'
    rpt = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        rpt.delete()
        return redirect('database:list')
    
    context = {
        "page": page,
        "object": rpt,
    }
    return render(request, "database/report_delete.html", context)

def report_done(request, srch_id):
    try:
        obj = Report.objects.get(pk=srch_id)
    except Report.DoesNotExist:
        raise Http404
    
    print(obj.option)
    
    if obj.option == 'Selesai':
        obj.option = 'Tinjau'
        obj.save()
        return redirect('database:list')
    
    obj.option = 'Selesai'
    obj.save()
    return redirect('database:list')

# Censorship CRUD

def censorship_create(request):
    page = 'censorship'
    form = RawCensorshipForm()

    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description')
        }
        
        form = RawCensorshipForm(form_data)
        if form.is_valid():
            print(form.cleaned_data)
            Censorship.objects.create(**form.cleaned_data)
            return redirect('database:list')
        else:
            print(form.errors)
    
    context = {
        'form': form,
        'page': page,
    }
    return render(request, 'database/report_form.html', context)

def censorship_edit(request, csp_id):
    page = 'csp_edit'
    try: 
        obj = Censorship.objects.get(pk=csp_id)
    except Censorship.DoesNotExist:
        raise Http404

    form = CensorshipForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        "form": form,
        "page": page,
    }
    return render(request, "database/report_form.html", context)

def censorship_delete(request, csp_id):
    page = 'csp_delete'
    censor = get_object_or_404(Censorship, pk=csp_id)
    
    if request.method == 'POST':
        censor.delete()
        return redirect('database:list')
    
    context = {
        "object": censor,
        "page": page,
    }
    return render(request, "database/report_delete.html", context)