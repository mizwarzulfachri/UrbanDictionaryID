from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import WordForm, RawWordForm, TagForm, RawTagForm

from .models import Word, Tag

import pyttsx3
# import gtts # Google Text To Speech only works when the audio is saved!

# Create your views here.

# CRUD for word 

@login_required(login_url='login')
def word_create(request):
    inform = RawWordForm()

    if request.method == "POST":
        form_data = {
            'word': request.POST.get('word'),
            'pronunciation': request.FILES.get('pronunciation'),
            'definition': request.POST.get('definition'),
            'tags': request.POST.get('tags'),
            'user': request.user,
         }
        
        inform = RawWordForm(form_data, request.FILES)
        if inform.is_valid():
            print(inform.cleaned_data)
            Word.objects.create(**inform.cleaned_data)
            return redirect('home')
        else:
            print(inform.errors)
    
    context = {
        'form': inform,
    }
    return render(request, "word/word_form.html", context)

def word_view(request, wrd_id):
    wrd = get_object_or_404(Word, id=wrd_id)

    context = {
        'object': wrd,
    }
    return render(request, "word/word_detail.html", context)

@login_required(login_url='login')
def word_edit(request, srch_id):
    try: 
        obj = Word.objects.get(pk=srch_id)
    except Word.DoesNotExist:
        raise Http404

    if request.user != obj.user: 
        return HttpResponse('<h1>You have no access to edit</h1>')

    form = WordForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        "form": form,
    }
    return render(request, "word/word_form.html", context)

@login_required(login_url='login')
def word_delete(request, wrd_id):
    page = 'word'
    wrd = get_object_or_404(Word, pk=wrd_id)
    
    if request.method == 'POST':
        wrd.delete()
        return redirect('home')
    
    context = {
        "object": wrd,
        "page": page,
    }
    return render(request, "word/word_delete.html", context)

# Word Pronunciation

def text_to_speech(request, pk):
    wrd = get_object_or_404(Word, pk=pk)
    obj = Word.objects.get(pk=pk)

    txt_speech = pyttsx3.init()
    txt_speech.say(obj)
    txt_speech.runAndWait()
    print(obj.word + " has been pronounced")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# CRUD for tags

def tag_create(request):
    inform = RawTagForm()

    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
         }
        
        inform = RawWordForm(form_data, request.FILES)
        if inform.is_valid():
            print(inform.cleaned_data)
            Tag.objects.create(**inform.cleaned_data)
            return redirect('database')
        else:
            print(inform.errors)
    
    context = {
        'form': inform,
    }
    return render(request, 'word/word_form.html', context)

def tag_edit(request, tag_id):
    try: 
        obj = Tag.objects.get(pk=tag_id)
    except Word.DoesNotExist:
        raise Http404

    form = TagForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        "form": form,
    }
    return render(request, "word/word_form.html", context)

def tag_delete(request, tag_id):
    page = 'tag'
    tag = get_object_or_404(Tag, pk=tag_id)
    
    if request.method == 'POST':
        tag.delete()
        return redirect('database')
    
    context = {
        "object": tag,
        "page": page,
    }
    return render(request, "word/word_delete.html", context)