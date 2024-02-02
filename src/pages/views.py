from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# App models
from word.models import Word, Tag

# Import
import random
import pyttsx3

# Create your views here.
def homepage(request, *args, **kwargs):
    page = 'homepage'

    # Search
    q = request.GET.get('s') if request.GET.get('s') != None else ''
    wordlist = Word.objects.filter(
        Q(word__icontains=q) # |
        # Q(user__username__icontains=q)
        ).order_by('-up', '?')

    # Search start with
    if request.GET.get('b') != None:
        q = request.GET.get('b') 
        wordlist = Word.objects.filter(Q(word__istartswith=q)).order_by('word', '-up')

    # Search by tags
    if request.GET.get('q') != None: 
        q = request.GET.get('q')  
        wordlist = Word.objects.filter(Q(tags__name__icontains=q)).order_by('-up', '?')

    # Search by ASCII
    if request.GET.get('a') != None: 
        wordlist = Word.objects.order_by('word')

    # Search by recent
    if request.GET.get('n') != None: 
        q = request.GET.get('n')  
        wordlist = Word.objects.order_by('-date')

    # Search by user 
    # if request.GET.get('u') != None: 
    #     q = request.GET.get('u')  
    #     wordlist = Word.objects.filter(Q(user__username__icontains=q)).order_by('-up', '?')

    queryset = Tag.objects.all().order_by('name')

    context = {
        "object_list": wordlist,
        "filter": queryset,
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
            messages.error(request, 'Nama user atau password salah')

    context = {'page': page,}
    return render(request, 'login_register.html', context)

def logout_pg(request):
    logout(request)
    return redirect('home')

def register_pg(request):
    page = 'register'

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error saat mendaftarkan user')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'login_register.html', context)

def user_pg(request, pk):
    page = 'user'

    user = get_object_or_404(User, id=pk)
    wordlist = Word.objects.filter(Q(user__username__icontains=user.username)).order_by('-up')
    word_count = wordlist.count()

    queryset = Tag.objects.all().order_by('name')

    context = {
        'user': user,
        'object_list': wordlist,
        'filter': queryset,
        'count': word_count,
        'page': page,
    }
    return render(request, 'homepage.html', context)

def about_pg(request, *args, **kwargs):
    return render(request, "about.html")