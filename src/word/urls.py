from django.urls import path

from .views import *

app_name = 'word'
urlpatterns = [
    # Word path
    path('<int:wrd_id>/', word_view, name='word'),
    path('speech/<int:pk>/', text_to_speech, name='speech'),
    path('up/<int:word_id>/', up, name='upvotes'),
    path('down/<int:word_id>', down, name='downvotes'),

    # Tag path
    path('tag', tag_create, name='tag'),
    path('tag-update/<int:tag_id>/', tag_edit, name='tag-update'),
    path('tag-delete/<int:tag_id>/', tag_delete, name='tag-delete'),

    # CRUD path
    path('create/', word_create, name='create'),
    path('edit/<int:srch_id>/', word_edit, name='edit'),
    path('delete/<int:wrd_id>/', word_delete, name='delete'),
]