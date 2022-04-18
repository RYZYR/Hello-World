import re
from django import http
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from .forms import *
from .models import *
import json
from .ThreadCamera import *
from datetime import datetime,timedelta
import random
from django.views.decorators.csrf import csrf_exempt

import requests
import time
import cv2
# Create your views here.
weekdayDic = {1:'周一',2:'周二',3:'周三',4:'周四',5:'周五'}
v = None
section = None

def detectVideo():
    global v
    global section
    if section is not None:
        section = None
    if v is not None:
        if v.is_record:
            v.stop_record()

def index(request):
    detectVideo()
    return render(request, 'srtpApp/index.html')

def newSecInfo(request):
    global v
    global section
    error_info = ''
    form = newSecInfoForm()
    if request.method == 'POST':
        if 'submit' in request.POST:
            form = newSecInfoForm(request.POST)
            if form.is_valid():
                courseID = form.cleaned_data['course_name']
                courseObj = Course.objects.get(id = courseID)
                weekNum = form.cleaned_data['week_num']
                weekdayNum = form.cleaned_data['weekday_num']
                sectionNum = form.cleaned_data['section_num']
                ipStr = "http://"+ form.cleaned_data['ip_addr'] +":8080/?action=stream"
                try:
                    sec = Section.objects.get(course_name=courseObj, week_num=weekNum, weekday_num=weekdayNum,
                                              section_num=sectionNum)
                except:
                    if v is None or section is not None:
                        detectVideo()
                        v = VideoCamera()
                    v.start_record()

                    section = Section(course_name = courseObj, week_num = weekNum, weekday_num = weekdayNum, section_num = sectionNum)
                    return render(request, 'srtpAPP/newSecInfo.html', {"form": form, 'showFlag': "True", 'ipStr':ipStr})
                else:
                    error_info = '已经创建了该课堂'

        elif 'delete' in request.POST:
            Section.objects.all().delete()
            return render(request, 'srtpAPP/newSecInfo.html', {"form":form,'message':"删除成功"})
        elif 'end' in request.POST:
        # 控制 识别程序停止 读取json格式数据
            v.stop_record()
            with open(os.getcwd()+r"\srtpApp\jsonData\data.json","r",encoding='utf8') as f:
                jsonData = json.load(f)
        #存储section数据到 Section表中
            if section is not None:
                section.capture_num = jsonData["countCapture"]
                section.save()
            elif section is None:
                return HttpResponseRedirect(reverse('srtpApp:newSecInfo'))
        # 解析json数据存入 Status数据表中
            stuObjs = Student.objects.all()
            for stuObj in stuObjs:
            #获取当前stuObj的学号stuID
                stuID = stuObj.stuID

                # 获取json数据
                focusTime = jsonData[stuID]["detect_success"]
                count = jsonData[stuID]["count"]
                start = datetime.strptime(jsonData["startTime"], '%Y-%m-%d %H:%M:%S')
                end = datetime.strptime(jsonData["endTime"], '%Y-%m-%d %H:%M:%S')
            #将数据存入status数据表
                status = Status()
                status.stuID = stuObj
                status.sectionID = section
                status.focus_num = focusTime
                status.unfocus_num = count - focusTime
                if count != 0:
                    stuStart = datetime.strptime(jsonData[stuID]["start"], '%Y-%m-%d %H:%M:%S')
                    stuEnd = datetime.strptime(jsonData[stuID]["end"], '%Y-%m-%d %H:%M:%S')
                    status.signin_bool = True
                    if (stuStart - start) > timedelta(seconds=101):
                        status.late_bool = True
                    if (end - stuEnd) > timedelta(seconds=10):
                        status.leaveEarly_bool = True
                elif count == 0:
                    status.signin_bool = False
                    status.late_bool = False
                    status.leaveEarly_bool = False

                status.save()

            return HttpResponseRedirect(reverse("srtpApp:index"))

    return render(request, 'srtpApp/newSecInfo.html', {"form":form, 'error_info':error_info, 'showFlag': ""})

def checkSec(request):
    detectVideo()
    form = checkSecForm()
    if request.method == 'POST':
        form = checkSecForm(request.POST)
        if form.is_valid():
            courseID = form.cleaned_data['course_name']
            courseObj = Course.objects.get(id = courseID)
            weekNum = form.cleaned_data['week_num']
            weekdayNum = form.cleaned_data['weekday_num']
            sectionNum = form.cleaned_data['section_num']
            try:
                sec = Section.objects.get(course_name = courseObj, week_num = weekNum, weekday_num = weekdayNum, section_num = sectionNum)
            except:
                return render(request, 'srtpApp/checkSec.html', {"form":form, "error_info":"未查询到该节课"})
            else:
                seq=(
                    'course='+str(courseObj.course_name), 
                    'weeks='+ str(weekNum), 
                    'weekday='+weekdayDic[int(weekdayNum)],
                    'sec='+str(sectionNum),
                    )
                getStr = '?' + '&'.join(seq)
                return HttpResponseRedirect(reverse('srtpApp:checkInfoURL', args=[sec.id])+getStr)
    return render(request, 'srtpApp/checkSec.html', {"form":form})

def checkSecInfo(request,secID):
    detectVideo()
    sec = Section.objects.get(id = secID)
    captureNum = sec.capture_num
    name=[]
    unfocus = []
    focus=[]
    unsign = ""
    late = ""
    early = ""
    statusObjs = Status.objects.filter(sectionID=sec)
    for statusObj in statusObjs:
        sName = str(statusObj.stuID.stuname)
        sfocus = statusObj.focus_num
        sunfocus = statusObj.unfocus_num
        name.append(sName)
        focus.append(sfocus)
        unfocus.append(sunfocus)
        if not statusObj.signin_bool:
            unsign += (" "+sName)
        if statusObj.late_bool:
            late += (" "+sName)
        if statusObj.leaveEarly_bool:
            early += (" "+sName)
    if not unsign: unsign="无"
    if not late: late="无"
    if not early: early="无"

    dic = {
        'name': json.dumps(name),
        'focus': json.dumps(focus),
        'unfocus': json.dumps(unfocus),
        'unsign': unsign,
        'late': late,
        'early': early,
        'captureNum': captureNum,
    }
    return render(request, 'srtpApp/checkSecInfo.html', dic)