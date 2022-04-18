from django.urls import path

from . import views

app_name = 'srtpApp'
urlpatterns = [
    path('', views.index, name='index'),                                            #首页
    path('newSecInfo/', views.newSecInfo, name = 'newSecInfo'),                     # 新建课堂
    path('checkSec/', views.checkSec, name='checkURL'),                             #查询
    path('checkSecInfo/<int:secID>/', views.checkSecInfo, name='checkInfoURL'),     #查询结果
]