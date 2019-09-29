"""blog URL Configuration

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
from django.urls import path,include
from . import views
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ceshi/', views.ceshi),
    path('about/', views.about),
    path('index/', views.index),
    path('listpic/', views.listpic),
    path('newslistpic/', views.newslistpic),
    re_path('newslistpic/(\d+)', views.newslistpic),
    path('base/', views.base),
    path('addarticle/', views.addarticle),
    path('fytest/', views.fytest),
    path('reqtest/', views.reqtest),
    path('formtest/', views.formtest),
    path('register/', views.register),
    path('csrfdemo/', views.csrfdemo),
    path('login/', views.login),
    path('ajaxget/', views.ajaxget),
    path('ajaxget_data/', views.ajaxget_data),
    path('checkusername/', views.checkusername),
    path('nameblur/', views.nameblur),
    path('ajaxget_demo/', views.ajaxget_demo),
    path('ajaxget_demo_data/', views.ajaxget_demo_data),
    path('ajaxpost_demo/', views.ajaxpost_demo),
    path('ajaxpost_demo_data/', views.ajaxpost_demo_data),
    path('login_demo/', views.login_demo),
    path('logout/', views.logout),
    path('ajaxget_blur/', views.ajaxget_blur),
    path('ajaxpost/', views.ajaxpost),
    path('ajaxpost_data/', views.ajaxpost_data),
    re_path('neirong/(?P<id>\d+)',views.neirong),
    path('ckeditor/',include('ckeditor_uploader.urls'))
]
