"""
URL configuration for UrbanDictionary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.contrib.auth import views as auth_views

from pages.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('word/', include('word.urls')),
    path('database/', include('database.urls')),

    # path('change-password/', auth_views.PasswordChangeView.as_view(), name="reset_password"),
    # path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name="reset_password"),
    
    # Forgot Password Paths
    path('reset_password/', auth_views.PasswordResetView.as_view(
            template_name='forgot_pass/change_password.html',
            success_url=reverse_lazy('password_reset_done'),
        ), 
        name="password_reset"
    ), #1
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_pass/sent_email.html'), name="password_reset_done"), #2
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='forgot_pass/reset_pass.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name="password_reset_confirm"
    ), #3
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='forgot_pass/complete_pass.html',
        ), 
        name="password_reset_complete"
    ), #4

    # Pages path
    path('', homepage, name='home'),
    path('login/', login_pg, name='login'),
    path('logout/', logout_pg, name='logout'),
    path('register/', register_pg, name='register'),
    path('user/<int:pk>/', user_pg, name='user'),
    path('about/', about_pg, name='about'),
]