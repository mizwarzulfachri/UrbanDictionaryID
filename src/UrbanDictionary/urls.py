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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.i18n import i18n_patterns, set_language

from django.contrib.auth import views as auth_views

from pages.views import *

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', set_language, name='set_language'),
    path('rosetta/', include('rosetta.urls')),
    path('word/', include('word.urls')),
    path('database/', include('database.urls')),

    # path('change-password/', auth_views.PasswordChangeView.as_view(), name="reset_password"),
    # path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name="reset_password"),
    
    # Forgot Password Paths
    path('reset_password/', auth_views.PasswordResetView.as_view(
            template_name='forgot_pass/request_password_change_password.html',
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

    # Change password
    path('<int:pk>/password/', ChangePasswordView.as_view(template_name='forgot_pass/change_password.html',), name="password_change"),

    # Pages path
    path('', homepage, name='home'),
    path('login/', login_pg, name='login'),
    path('logout/', logout_pg, name='logout'),
    path('register/', register_pg, name='register'),
    path('user_del/<int:pk>/', del_usr, name='delete_usr'),
    path('user-edit/', UserEditView.as_view(), name=('edit_usr')),
    path('user/<int:pk>/', user_pg, name='user'),
    # path('about/', about_pg, name='about'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)