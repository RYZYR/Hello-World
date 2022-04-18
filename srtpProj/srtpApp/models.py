from ast import Mod
from calendar import FRIDAY, THURSDAY, TUESDAY, WEDNESDAY
from pyexpat import model
from random import choices
from statistics import mode
from tabnanny import verbose
from xml.etree.ElementTree import tostring
from django.db import models

# Create your models here.

class ClassGrade(models.Model):
    class_name = models.CharField(max_length=256)
    def __str__(self):
        return self.class_name

class Student(models.Model):
    #主键
    stuID = models.CharField(max_length=16, verbose_name="Student ID",primary_key=True)
    stuname = models.CharField(max_length=32, verbose_name='student\'s name')
    class_name = models.ForeignKey(ClassGrade, on_delete=models.CASCADE)

    def __str__(self):
        return self.stuID

class Course(models.Model):
    course_name = models.CharField(max_length=64,verbose_name="Course Name")
    def __str__(self):
        return self.course_name

class Section(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 如需要设置integerField的最大最小值需要使用   验证器: https://docs.djangoproject.com/zh-hans/4.0/ref/validators/#django.core.validators.MinValueValidator
    #1-18为有效值
    week_num = models.IntegerField(verbose_name='Which week')
    # 枚举类
    class Weekday(models.IntegerChoices):
        Monday = 1, '周一'
        TUESDAY = 2, '周二'
        WEDNESDAY = 3, '周三'
        THURSDAY = 4, '周四'
        FRIDAY = 5, '周五'
    weekday_num = models.IntegerField(choices = Weekday.choices, verbose_name='Which day in a week')
    section_num = models.IntegerField(verbose_name='Which section')
    capture_num = models.IntegerField("All capture times",default=0)
    class Meta:
        unique_together = (('course_name','week_num','weekday_num','section_num'),)
    def __str__(self) -> str:
        return "课堂ID:"+str(self.id)
    

class Status(models.Model):
    #主键ID自动生成
    stuID = models.ForeignKey(Student, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    focus_num = models.IntegerField(verbose_name="Focus Times")
    unfocus_num = models.IntegerField('unFocus Times', default=0)
    signin_bool = models.BooleanField('Sign in?')
    late_bool = models.BooleanField('late?',default=False)
    leaveEarly_bool = models.BooleanField('leave early?',default=False)
    signin_time = models.DateTimeField('Time of sign in',null=True, blank=True)
    signout_time = models.DateTimeField('Time of sign out',null=True, blank=True)
    def __str__(self) -> str:
        return str(self.stuID) + '-' + str(self.signin_bool)
