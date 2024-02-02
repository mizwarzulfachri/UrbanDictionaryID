from django.urls import path 

from .views import database_pg

app_name = 'database'
urlpatterns = [
    path('', database_pg, name='database'),
    # path('report/', report_pg, name='report'),
]