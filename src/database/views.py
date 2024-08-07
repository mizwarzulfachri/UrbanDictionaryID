from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.translation import get_language
from datetime import datetime, timedelta
from django.utils.translation import gettext as _

from .forms import ReportForm, RawReportForm, CensorshipForm, RawCensorshipForm

from .models import Report, Censorship

# App models
from word.models import Word, Tag

# Create your views here.
# Database homepage
@login_required(login_url='login')
def database_pg(request, *args, **kwargs):
    page = 'database'

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    # Dashboard Page
    rcnt_wrd = Word.objects.all().order_by("-date")
    last_week = datetime.now() - timedelta(days=7)
    two_weeks = datetime.now() - timedelta(weeks=2)
    last_year = datetime.now() - timedelta(weeks=52)

    # Graph of the tags being used since a week ago
    tag_week_counts = Tag.objects.annotate(
        word_count=Count('word_tag', filter=Q(word_tag__date__gte=last_week)))

    tag_week_percentages = {}
    top_recent_tags = None
    top_tpercentage = 0
    total_tag_week = 0

    for tag_week_count in tag_week_counts:
        total_tag_week = total_tag_week + tag_week_count.word_count

    if total_tag_week != 0:
        for tag_week_count in tag_week_counts:
            tag = tag_week_count.name
            count = tag_week_count.word_count
            percentage = (count / total_tag_week) * 100
            tag_week_percentages[tag] = percentage

            if percentage > top_tpercentage:
                top_tpercentage = percentage
                top_recent_tags = tag

    # Graph of the tags being used since a year ago
    tag_year_counts = Tag.objects.annotate(
        word_count=Count('word_tag', filter=Q(word_tag__date__gte=last_year)))
    
    tag_year_percentages = {}
    top_year_tags = None
    top_ytpercentage = 0
    total_tag_year = 0

    for tag_year_count in tag_year_counts:
        total_tag_year = total_tag_year + tag_year_count.word_count

    if tag_year_count != 0:
        for tag_year_count in tag_year_counts:
            tag = tag_year_count.name
            count = tag_year_count.word_count
    
            percentage = (count / total_tag_year) * 100
            tag_year_percentages[tag] = percentage
    
            if percentage > top_ytpercentage:
                top_ytpercentage = percentage
                top_year_tags = tag

    # Word Page
    wordlist = Word.objects.all().order_by('word')

    # User Page
    user = get_user_model()
    userlist = user.objects.all().order_by('-date_joined')
    
    # Report Page
    reportlist = Report.objects.filter(Q(option__icontains="Tinjau")).order_by("-date")
    donelist = Report.objects.filter(Q(option__icontains="Selesai")).order_by("date")
    censorlist = Censorship.objects.all().order_by('name')
    countrpt = reportlist.count()

    rcnt_rpt = Report.objects.filter(date__gte=two_weeks)
    category_counts = rcnt_rpt.values('category').annotate(count=Count('category'))
    total_reports = rcnt_rpt.count()

    category_percentages = {}
    top_category = None
    top_percentage = 0

    for category_count in category_counts:
        category = category_count['category']
        count = category_count['count']
        percentage = (count / total_reports) * 100
        category_percentages[category] = percentage

        if percentage > top_percentage:
            top_percentage = percentage
            top_category = category

    if top_category:
        translated_top_category = _(top_category)

    # Tag Page
    current_language = get_language()
    taglist = Tag.objects.active_translations(current_language).order_by(
        'translations__name' 
        ).filter(Q(translations__language_code__icontains=current_language))
    
    total_tag_count = Tag.objects.annotate(
        tag_counter=Count('word_tag')
    )
    total_queryset = total_tag_count.order_by('-tag_counter').exclude(translations__name='Vulgar')

    # Search Filters
    if request.GET.get('s') != None:
        q = request.GET.get('s')
        wordlist = Word.objects.filter(
            Q(word__istartswith=q) 
            ).order_by('word')
        
    # Search by ASCII
    if request.GET.get('a') != None: 
        wordlist = Word.objects.order_by('word')
        
    # Search by date
    if request.GET.get('n') != None: 
        q = request.GET.get('n')  
        wordlist = Word.objects.order_by('-date')

    if request.GET.get('t') != None: 
        q = request.GET.get('t')
        wordlist = Word.objects.filter(
            Q(tags__translations__name__icontains=q)
            ).order_by('word')

    if request.GET.get('u') != None:
        q = request.GET.get('u')
        userlist = User.objects.filter(
            Q(username__istartswith=q)
            ).order_by('username')

    context = {
        "uobject": userlist,
        "wobject": wordlist,
        "recentw": rcnt_wrd,
        "tobject": taglist,
        "counttag": total_queryset,
        "robject": reportlist,
        "done": donelist,
        "censored": censorlist,
        "count": countrpt,
        "top_tag_per": top_tpercentage,
        "top_rtag": top_recent_tags,
        "top_ytag_per": top_ytpercentage,
        "top_ytag": top_year_tags,
        "top_percent": top_percentage,
        "top_categor": translated_top_category,
        "page": page,
    }
    return render(request, "database/database.html", context)

# Report List
# @login_required(login_url='login')
# def report_list(request):
#     page = "list"

#     if not request.user.is_superuser:
#         raise Http404

#     reportlist = Report.objects.filter(Q(option__icontains="Tinjau")).order_by("date")
#     donelist = Report.objects.filter(Q(option__icontains="Selesai")).order_by("date")
#     censorlist = Censorship.objects.all().order_by('name')

#     context = {
#         "robject": reportlist,
#         "done": donelist,
#         "censored": censorlist,
#         "page": page,
#     }
#     return render(request, "database/database.html", context)

# View Reports 
@login_required(login_url='login')
def report_view(request, srch_id):
    page = 'view'
    report = get_object_or_404(Report, pk=srch_id)

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    context = {
        'report': report,
        'page': page,
    }
    return render(request, "database/report.html", context)

# Report Form
@login_required(login_url='login')
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

# Report Delete
@login_required(login_url='login')
def report_del(request, pk):
    page = 'delete'
    rpt = get_object_or_404(Report, pk=pk)

    if request.user != rpt.user and not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if request.method == 'POST':
        rpt.delete()
        
        if request.user.is_superuser:
            base_url = reverse('database:database')
            url = f"{base_url}#Report"
            return redirect(url)
        else:
            return redirect('report_usr', request.user.pk)
    
    context = {
        "page": page,
        "object": rpt,
    }
    return render(request, "database/report_delete.html", context)

# Report Mark as Done
@login_required(login_url='login')
def report_done(request, srch_id):
    try:
        obj = Report.objects.get(pk=srch_id)
    except Report.DoesNotExist:
        raise Http404

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')
    
    print(obj.option)
    
    if obj.option == 'Selesai':
        obj.option = 'Tinjau'
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    obj.option = 'Selesai'
    obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Censorship CRUD
@login_required(login_url='login')
def censorship_create(request):
    page = 'censorship'
    form = RawCensorshipForm()

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description')
        }
        
        form = RawCensorshipForm(form_data)
        if form.is_valid():
            print(form.cleaned_data)
            Censorship.objects.create(**form.cleaned_data)
            base_url = reverse('database:database')
            url = f"{base_url}#Report"
            return redirect(url)
        
        else:
            print(form.errors)
    
    context = {
        'form': form,
        'page': page,
    }
    return render(request, 'database/report_form.html', context)

@login_required(login_url='login')
def censorship_edit(request, csp_id):
    page = 'csp_edit'
    try: 
        obj = Censorship.objects.get(pk=csp_id)
    except Censorship.DoesNotExist:
        raise Http404

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    form = CensorshipForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        base_url = reverse('database:database')
        url = f"{base_url}#Report"
        return redirect(url)

    context = {
        "form": form,
        "page": page,
    }
    return render(request, "database/report_form.html", context)

@login_required(login_url='login')
def censorship_delete(request, csp_id):
    page = 'csp_delete'
    censor = get_object_or_404(Censorship, pk=csp_id)

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')
    
    if request.method == 'POST':
        censor.delete()
        base_url = reverse('database:database')
        url = f"{base_url}#Report"
        return redirect(url)
    
    context = {
        "object": censor,
        "page": page,
    }
    return render(request, "database/report_delete.html", context)