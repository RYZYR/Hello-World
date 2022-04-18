"""srtpProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from argparse import Namespace
from tkinter.font import names
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView 
from srtpApp import views
urlpatterns = [
    path('', RedirectView.as_view(url='/app/')),        #访问http://127.0.0.1:8000/时自动重定向到 http://127.0.0.1:8000/app/
    path('app/', include('srtpApp.urls',namespace='srtpApp')),              #路由分配到 srtpApp的urlConf
    path('admin/', admin.site.urls),
]
