from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

class LessonAdmin(SummernoteModelAdmin):
    # Укажите поля модели, которые будут использовать Summernote
    summernote_fields = ('content',)

admin.site.register([Teacher, Pupil, Transaction, User])
admin.site.register(Lesson, LessonAdmin)
admin.site.register([Answer, Question, TestResult])