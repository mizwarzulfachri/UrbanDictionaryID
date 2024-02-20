from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from difflib import SequenceMatcher

from .forms import WordForm, RawWordForm, TagForm, RawTagForm

from .models import Word, Tag
from database.models import Censorship

import pyttsx3
# import gtts # Google Text To Speech only works when the audio is saved!

# Create your views here.

# CRUD for word 

@login_required(login_url='login')
def word_create(request):
    page = "word"
    form = RawWordForm()

    if request.method == "POST":
        form_data = {
            'word': request.POST.get('word'),
            'pronunciation': request.FILES.get('pronunciation'),
            'definition': request.POST.get('definition'),
            'tags': request.POST.getlist('tags'),
            'user': request.user,
        }

        form = RawWordForm(form_data, request.FILES)
        if form.is_valid():        
            # Word save 
            w = Word(
                word = form.cleaned_data['word'],
                pronunciation = form.cleaned_data['pronunciation'],
                definition = form.cleaned_data['definition'],
                user = form.cleaned_data['user'],
            )

            w.save()
            tags = form.cleaned_data['tags'],
            w.tags.set(request.POST.getlist('tags'))
            
            wrd = form.cleaned_data['word']
            censored_words = Censorship.objects.values_list('name', flat=True)

             # Word censorship checks
            for cword in censored_words:
                if censor_word(wrd.lower(), cword.lower()):
                    tag_selected = Tag.objects.get(name='Vulgar')
                    w.tags.set([tag_selected])
                    print(wrd + ' is found in the censorship database')
                    break
            return redirect('home')
        else:
            print(form.cleaned_data)
            print(form.errors)
    
    context = {
        'form': form,
        'page': page,
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

    if request.user != obj.user and not request.user.is_superuser: 
        return HttpResponse('<h1>Anda tidak dapat access</h1>')

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
    
    if request.user != wrd.user and not request.user.is_superuser: 
        return HttpResponse('<h1>Anda tidak dapat access</h1>')

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
# Only accessible to the admin

def tag_create(request):
    page = 'tag'
    inform = RawTagForm()

    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
        }
        
        inform = RawTagForm(form_data)
        if inform.is_valid():
            print(inform.cleaned_data)
            Tag.objects.create(**inform.cleaned_data)
            return redirect('database:database')
        else:
            print(inform.errors)
    
    context = {
        'form': inform,
        'page': page,
    }
    return render(request, 'word/word_form.html', context)

def tag_edit(request, tag_id):
    page = 'edit'
    try: 
        obj = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist:
        raise Http404

    form = TagForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        "form": form,
        "page": page,
    }
    return render(request, "word/word_form.html", context)

def tag_delete(request, tag_id):
    page = 'tag'
    tag = get_object_or_404(Tag, pk=tag_id)
    
    if request.method == 'POST':
        tag.delete()
        return redirect('database:database')
    
    context = {
        "object": tag,
        "page": page,
    }
    return render(request, "word/word_delete.html", context)

# Word Censorship

def censor_word(word1, word2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, word1, word2).ratio()
    return similarity_ratio >= threshold