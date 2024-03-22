from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from difflib import SequenceMatcher
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .forms import WordForm, RawWordForm, TagForm, RawTagForm

from .models import Word, Tag, Upvotes, Downvotes, Pronounce
from database.models import Censorship

import os
import pyttsx3 # Text to speech API
from gtts import gTTS # Google Text To Speech only works when the audio is saved!
from pygame import mixer

# Create your views here.

# CRUD for word 

@login_required(login_url='login')
def word_create(request):
    page = "word"
    form = RawWordForm()

    if request.method == "POST":
        form_data = {
            'word': request.POST.get('word'),
            # 'pronunciation': request.FILES.get('pronunciation'),
            'definition': request.POST.get('definition'),
            'tags': request.POST.getlist('tags'),
            'user': request.user,
        }

        form = RawWordForm(form_data, request.FILES)
        if form.is_valid(): 
            # Pronounce 
            try:
                p = get_object_or_404(Pronounce, name__icontains=form.cleaned_data['word'])
                print(form.cleaned_data['word'] + " has been successfully linked")
            except Http404:
                obj = gTTS(text=form.cleaned_data['word'], lang='id', slow=False)

                file_name = "src/media/" + form.cleaned_data['word'] + ".mp3"
                obj.save(file_name)

                p = Pronounce(name = (form.cleaned_data['word']).lower())

                with open(file_name, 'rb') as f:
                    file_content = f.read()

                p.pronunciation.save(file_name, ContentFile(file_content))
                p.save()
                
                print(form.cleaned_data['word'] + " has been successfully created")
                os.remove(file_name)

            # Word save 
            w = Word(
                word = form.cleaned_data['word'],
                pronunciation = p,
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
    page = "word"
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
        "page": page,
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

# Word Vote
@login_required(login_url='login')
def up(request, word_id):
    user = request.user
    word = get_object_or_404(Word, pk=word_id)

    up_currently = word.up
    up = Upvotes.objects.filter(user=user, word=word).count()
    down_currently = word.down
    down = Downvotes.objects.filter(user=user, word=word).count()
    
    if not up:
        up = Upvotes.objects.create(user=user, word=word)
        up_currently = up_currently + 1
    else:
        up = Upvotes.objects.filter(user=user, word=word).delete()
        up_currently = up_currently - 1

    word.up = up_currently
    word.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def down(request, word_id):
    user = request.user
    word = get_object_or_404(Word, pk=word_id)

    down_currently = word.down
    down = Downvotes.objects.filter(user=user, word=word).count()
    up_currently = word.up
    up = Upvotes.objects.filter(user=user, word=word).count()
    
    if not down:
        down = Downvotes.objects.create(user=user, word=word)
        down_currently = down_currently + 1
    else:
        down = Downvotes.objects.filter(user=user, word=word).delete()
        down_currently = down_currently - 1

    word.down = down_currently
    word.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Word Pronunciation

def text_to_speech(request, pk):
    wrd = get_object_or_404(Word, pk=pk)
    
    file_path = wrd.pronunciation.pronunciation.path

    if file_path:
        mixer.init()

        mixer.music.load(file_path)
        mixer.music.play()

    print(f"{wrd.word} has been pronounced")

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