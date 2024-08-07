from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from difflib import SequenceMatcher
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .forms import WordForm, RawWordForm, TagForm, RawTagForm

from .models import Word, Tag, Upvotes, Downvotes, Pronounce
from database.models import Censorship

from io import BytesIO
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
            'definition': request.POST.get('definition'),
            'tags': request.POST.getlist('tags'),
            'user': request.user,
        }

        form = RawWordForm(form_data)
        if form.is_valid(): 
            # Pronounce 
            try:
                p = get_object_or_404(Pronounce, name__iexact=form.cleaned_data['word'])
                print(form.cleaned_data['word'] + " has been successfully linked")
            except Http404:
                obj = gTTS(text=form.cleaned_data['word'], lang='id', slow=False)

                mp3_fp = BytesIO()
                obj.write_to_fp(mp3_fp)

                mp3_fp.seek(0)
                pronunciation_file = ContentFile(mp3_fp.read(), name=form.cleaned_data['word'] + ".mp3")

                p = Pronounce(name=form.cleaned_data['word'].lower(), pronunciation=pronunciation_file)
                p.save()

                print(f"Successfully saved {form.cleaned_data['word']}.mp3 to {settings.MEDIA_ROOT}")          
                print(form.cleaned_data['word'] + " has been successfully created")

            # Word save 
            w = Word(
                word = form.cleaned_data['word'],
                pronunciation = p,
                definition = form.cleaned_data['definition'],
                user = form.cleaned_data['user'],
            )
            w.save()

            tags = form.cleaned_data['tags']
            w.tags.set(request.POST.getlist('tags'))

            tag_selected =[tag.name for tag in tags]
            print("Tag :", tag_selected)
            
            if 'Vulgar' in [tag.name for tag in tags]:
                w.visibility = 'Vulgar'
                w.save()

                print(w.word + ' is labelled as Vulgar')
                return redirect('home')

            wrd = form.cleaned_data['word']
            censored_words = Censorship.objects.values_list('name', flat=True)

            # Word censorship checks
            for cword in censored_words:
                if censor_word(wrd.lower(), cword.lower()):
                    w.visibility = 'Vulgar'
                    w.save()

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
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    form = WordForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('word:word', srch_id)

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
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

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
    down_currently = word.down

    # down_currently = word.down
    # down = Downvotes.objects.filter(user=user, word=word).count()
    
    if Upvotes.objects.filter(user=user, word=word).exists():
        Upvotes.objects.filter(user=user, word=word).delete()
        up_currently -= 1
    else:
        Upvotes.objects.create(user=user, word=word)
        up_currently += 1

        # if Downvotes.objects.filter(user=user, word=word).exists():
        #    Downvotes.objects.filter(user=user, word=word).delete()
        #    down_currently -= 1

    word.up = up_currently
    word.save()
    return JsonResponse({'up': up_currently})

@login_required(login_url='login')
def down(request, word_id):
    user = request.user
    word = get_object_or_404(Word, pk=word_id)
    down_currently = word.down
    up_currently = word.up

    # up_currently = word.up
    # up = Upvotes.objects.filter(user=user, word=word).count()
    
    if Downvotes.objects.filter(user=user, word=word).exists():
        Downvotes.objects.filter(user=user, word=word).delete()
        down_currently -= 1
    else:
        Downvotes.objects.create(user=user, word=word)
        down_currently += 1

        # if Upvotes.objects.filter(user=user, word=word).exists():
        #    Upvotes.objects.filter(user=user, word=word).delete()
        #    up_currently -= 1

    word.down = down_currently
    word.save()
    return JsonResponse({'down': down_currently})

# Visibility
@login_required(login_url='login')
def vulgar(request, wrd_id):
    wrd = get_object_or_404(Word, pk=wrd_id)

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 505</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if wrd.visibility == 'Vulgar':
        wrd.visibility = 'Public'
        wrd.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    wrd.visibility = 'Vulgar'
    wrd.save()
    print(wrd.word + ' is Hidden!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def hide(request, wrd_id):
    wrd = get_object_or_404(Word, pk=wrd_id)

    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 505</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if wrd.visibility == 'Hidden':
        wrd.visibility = 'Public'
        wrd.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    wrd.visibility = 'Hidden'
    wrd.save()
    print(wrd.word + ' is Hidden!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Word Pronunciation
# Replaced by javascript
def text_to_speech(request, pk):
    wrd = get_object_or_404(Word, pk=pk)
    
    file_path = wrd.pronunciation.pronunciation.path

    if file_path:
        mixer.init()

        mixer.music.load(file_path)
        mixer.music.play()

    print(f"{wrd.word} has been pronounced")
    print(f"{wrd.pronunciation.pronunciation} is the source audio!")

    return redirect('word:word', pk)

# CRUD for tags
# Only accessible to the admin
@login_required(login_url='login')
def tag_create(request):
    page = 'tag'
    inform = RawTagForm()
    
    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
        }
        
        inform = RawTagForm(form_data)
        if inform.is_valid():
            print(inform.cleaned_data)
            Tag.objects.create(**inform.cleaned_data)
            base_url = reverse('database:database')
            url = f"{base_url}#Tag"
            return redirect(url)
        else:
            print(inform.errors)
    
    context = {
        'form': inform,
        'page': page,
    }
    return render(request, 'word/word_form.html', context)

@login_required(login_url='login')
def tag_edit(request, tag_id):
    page = 'edit'
    
    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')

    try: 
        obj = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist:
        raise Http404

    form = TagForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        base_url = reverse('database:database')
        url = f"{base_url}#Tag"
        return redirect(url)

    context = {
        "form": form,
        "page": page,
    }
    return render(request, "word/word_form.html", context)

@login_required(login_url='login')
def tag_delete(request, tag_id):
    page = 'tag'
    tag = get_object_or_404(Tag, pk=tag_id)
    
    if not request.user.is_superuser:
        return HttpResponse('<h1>Error 404</h1><script>setTimeout(function(){ window.location.href = "' + reverse('home') + '"; }, 5000);</script>')
    
    if request.method == 'POST':
        tag.delete()
        base_url = reverse('database:database')
        url = f"{base_url}#Tag"
        return redirect(url)
    
    context = {
        "object": tag,
        "page": page,
    }
    return render(request, "word/word_delete.html", context)

# Word Censorship
def censor_word(word1, word2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, word1, word2).ratio()
    return similarity_ratio >= threshold