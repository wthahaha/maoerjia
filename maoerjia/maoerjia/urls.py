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

from maoerjia.route import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/auth/signup', user_signup, name='auth_signup'),
    # path('api/auth/login', user_login, name='auth_login'),
    # path('api/auth/verify', verify_token, name='token_verify'),
    # path('api/auth/change_password', change_password, name='change_password'),

    path('api/home_basic_info/<int:pk>', HomeBasicInfo_DETAIL, name='home_basic_info_detail_view'),
    path('api/home_basic_info/', HomeBasicInfo_LIST, name='home_basic_info_list_view'),
]
