from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.db.models import Q, Count
from django.views import generic
from datetime import datetime, timedelta

# App models
from word.models import Word, Tag
from database.models import Report
from .forms import RegisterUserForm, EditProfileForm

# Import
import random
import pyttsx3
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def homepage(request, *args, **kwargs):
    page = 'homepage'
    
    q = request.GET.get('') if request.GET.get('') != None else ''
    wordlist = Word.objects.filter(
        Q(word__icontains=q) 
        ).exclude(Q(visibility='Vulgar') | Q(visibility='Hidden')).order_by('-up', 'down', '?')

    # Search
    if request.GET.get('s') != None:
        q = request.GET.get('s')
        wordlist = Word.objects.filter(
            Q(word__istartswith=q) 
            ).exclude(visibility='Hidden').order_by('-up', 'down')
    
    # Search start with
    if request.GET.get('b') != None:
        q = request.GET.get('b') 
        wordlist = Word.objects.filter(
            Q(word__istartswith=q)
            ).exclude(Q(visibility='Vulgar') | Q(visibility='Hidden')).order_by('word', '-up')

    # Search by tags
    if request.GET.get('q') != None: 
        q = request.GET.get('q')  
        wordlist = Word.objects.filter(
            Q(tags__translations__name__iexact=q)
            ).exclude(Q(visibility='Vulgar') | Q(visibility='Hidden')).order_by('-up', 'down', '?')

    # Search by ASCII
    if request.GET.get('a') != None: 
        wordlist = Word.objects.exclude(
            Q(visibility='Vulgar') | Q(visibility='Hidden')
        ).order_by('word')

    # Search by recent
    if request.GET.get('n') != None: 
        q = request.GET.get('n')  
        wordlist = Word.objects.exclude(
            Q(visibility='Vulgar') | Q(visibility='Hidden')
        ).order_by('-date')

    # Search by user 
    # if request.GET.get('u') != None: 
    #     q = request.GET.get('u')  
    #     wordlist = Word.objects.filter(Q(user__username__icontains=q)).order_by('-up', '?')

    # Tags Order
    recent = datetime.now() - timedelta(days=7)
    
    tags_count = Tag.objects.annotate(
        word_count=Count('word_tag', filter=Q(word_tag__date__gte=recent))
        )
    queryset = tags_count.order_by('-word_count').exclude(translations__name='Vulgar')

    total_tag_count = Tag.objects.annotate(
        tag_counter=Count('word_tag')
    )
    total_queryset = total_tag_count.order_by('-tag_counter').exclude(translations__name='Vulgar')
    
    # for tag in tags_count:
    #     print(f"Tag: {tag.name}, Word Count: {tag.word_count}")
    # queryset = Tag.objects.all().order_by('name').exclude(name='Vulgar') # Base tag query

    context = {
        "object_list": wordlist,
        "filter": queryset,
        "count_word": total_queryset,
        "query": q,
        "page": page,
    }
    return render(request, "homepage.html", context)

def login_pg(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        try:
            login(request, user) 
            return redirect('home')   
        except:
            messages.error(request, _('Nama user atau kata sandi salah'))

    context = {'page': page,}
    return render(request, 'login_register.html', context)

def logout_pg(request):
    logout(request)
    return redirect('home')

def register_pg(request):
    page = 'register'

    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            if 'Admin' in request.POST.getlist('checked'):
                user.is_superuser = True
                user.save()
                print('user is an admin')
            
            if user.is_superuser:
                base_url = reverse('database:database')
                url = f"{base_url}#User"
                return redirect(url)
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, _('Error saat mendaftarkan user'))

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'login_register.html', context)

def del_usr(request, pk):
    page = 'user'
    user = get_object_or_404(User, pk=pk)

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 505</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if request.method == 'POST':
        user.delete()
        base_url = reverse('database:database')
        url = f"{base_url}#User"
        return redirect(url)

    context = {
        "object": user,
        "page": page,
    }
    return render(request, "database/report_delete.html", context)
    

def user_pg(request, pk):
    page = 'user'

    user = get_object_or_404(User, id=pk)
    wordlist = Word.objects.filter(
        Q(user__username__icontains=user.username)
        ).exclude(
            Q(visibility='Vulgar') | Q(visibility='Hidden')
            ).order_by('-up')

    if user == request.user:
        wordlist = Word.objects.filter(Q(user__username__icontains=user.username)).order_by('-up')

    # Count Word List
    count_submit = wordlist.count()

    # Tags Order
    recent = datetime.now() - timedelta(days=7)
    
    tags_count = Tag.objects.annotate(word_count=Count('word_tag', filter=Q(word_tag__date__gte=recent)))
    queryset = tags_count.order_by('-word_count').exclude(translations__name='Vulgar')

    total_tag_count = Tag.objects.annotate(
        tag_counter=Count('word_tag')
    )
    total_queryset = total_tag_count.order_by('-tag_counter').exclude(translations__name='Vulgar')
    
    # queryset = Tag.objects.all().order_by('name').exclude(name='Vulgar')

    context = {
        'user': user,
        'object_list': wordlist,
        'count_submit': count_submit,
        "filter": queryset,
        "count_word": total_queryset,
        'page': page,
    }
    return render(request, 'homepage.html', context)

def report_user(request, pk):
    user = get_object_or_404(User, id=pk)
    
    if request.user != user:
        return HttpResponse('<h1>Error 505</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    reportlist = Report.objects.filter(Q(user__username__icontains=user.username)).order_by("-date")
    
    count_submit = reportlist.count()

    # report_count = Report.objects.annotate(users_report=Count('category', filter=Q(user__username__icontains=user.username)))
    # queryset = report_count.order_by('-users_report')

    context = {
        'user': user,
        'instance': reportlist,
        'count': count_submit,
        # 'count_report': queryset,
    }
    return render(request, 'database/user_report_list.html', context)

# Edit user profile 
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'profile.html'
    
    def get_object(self):
        return self.request.user

    def get_success_url(self):
        success_url = reverse_lazy('user', kwargs={'pk': self.request.user.pk})
        logger.debug(f'Success URL: {success_url}')
        return success_url

# About Page 
# def about_pg(request, *args, **kwargs):
#     return render(request, "about.html")

# Change Password
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    
    def get_success_url(self):
        success_url = reverse_lazy('user', kwargs={'pk': self.request.user.pk})
        logger.debug(f'Success URL: {success_url}')
        return success_url