from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('course_name',)
    list_display = ('course_name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = ('stuID',('stuname', 'class_name'))
    list_display = ('stuID','stuname', 'class_name')
    list_filter = ('class_name',)

@admin.register(ClassGrade)
class ClassGradeAdmin(admin.ModelAdmin):
    fields = ('class_name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    fields = ('stuID','sectionID','focus_num','signin_bool','signin_time')
    list_display = ('stuID','sectionID','focus_num','unfocus_num','signin_bool','late_bool','leaveEarly_bool','signin_time','signout_time')
    list_filter = ('sectionID',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id','course_name','week_num','weekday_num','section_num','capture_num')

