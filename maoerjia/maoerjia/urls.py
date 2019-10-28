"""ansibleWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from apps.core.api.auth_view import (
    change_password,
    user_signup,
    user_login,
    verify_token
)

from apps.route import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup', user_signup, name='auth_signup'),
    path('api/auth/login', user_login, name='auth_login'),
    path('api/auth/verify', verify_token, name='token_verify'),
    path('api/auth/change_password', change_password, name='change_password'),

    path('api/teams/<int:pk>', TEAM_DETAIL, name='team_detail_view'),
    path('api/search/teams', TEAM_SEARCH, name="team_select_search"),
    path('api/teams/', TEAM_LIST, name='team_list_view'),

    path('api/credentials/', CREDENTIALS_LIST, name='securey_key_view'),
    path('api/credentials/<str:pk>', CREDENTIALS_DETAIL,
         name='securey_key_view_detail'),
]
