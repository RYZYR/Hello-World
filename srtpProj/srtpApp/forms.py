from secrets import choice
from turtle import textinput

from .public import *

from django import forms
from .models import Course

class newSecInfoForm(forms.Form):
    course_name = forms.ChoiceField(choices=(),widget=forms.Select(attrs={'style':'margin-left:30px;width:150px'}))
    week_num = forms.ChoiceField(choices=TupleClass.weekTuple(),widget=forms.Select(attrs={'style':'margin-left:58px;width:150px'}))
    weekday_num = forms.ChoiceField(choices=TupleClass.weekdayTuple,widget=forms.Select(attrs={'style':'margin-left:58px;width:150px'}))
    section_num = forms.ChoiceField(choices=TupleClass.secTuple(),widget=forms.Select(attrs={'style':'margin-left:58px;width:150px'}))
    ip_addr = forms.CharField(widget=forms.TextInput(attrs={'style':'width:150px;margin-left:4px'}))
    def __init__(self, *args, **kwargs):
        super(newSecInfoForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].choices = Course.objects.all().values_list('id','course_name') 

class checkSecForm(forms.Form):
    course_name = forms.ChoiceField(choices=(),widget=forms.Select(attrs={'class':'form-control','style':'width:400px;'}))
    week_num = forms.ChoiceField(choices=TupleClass.weekTuple(),widget=forms.Select(attrs={'class':'form-control','style':'width:400px;'}))
    weekday_num = forms.ChoiceField(choices=TupleClass.weekdayTuple,widget=forms.Select(attrs={'class':'form-control','style':'width:400px;'}))
    section_num = forms.ChoiceField(choices=TupleClass.secTuple(),widget=forms.Select(attrs={'class':'form-control','style':'width:400px;'}))

    def __init__(self, *args, **kwargs):
        super(checkSecForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].choices = Course.objects.all().values_list('id','course_name')
