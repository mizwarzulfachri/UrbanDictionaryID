from django.urls import path 

from .views import *

app_name = 'database'
urlpatterns = [
    path('', database_pg, name='database'),

    # Report CRD, there is no update
    path('list/', report_list, name='list'),
    path('view/<int:srch_id>/', report_view, name='view'),
    path('report/<int:pk>/', form_rppg, name='form'),
    path('done/<int:srch_id>/', report_done, name='done'),
    path('delete/<int:pk>/', report_del, name='delete'),

    # Censor CRUD
    path('censored/', censorship_create, name='censor-create'),
    path('censored-edit/<int:csp_id>/', censorship_edit, name='censor-edit'),
    path('censored-delete/<int:csp_id>/', censorship_delete, name='censor-delete'),
]