from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ExportMixin

from .models import *

# class LessonAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content',)

admin.site.register([Teacher, Pupil, Transaction, User, Operator, Lesson])
# admin.site.register(Lesson, LessonAdmin)
admin.site.register([Answer, Question, TestResult])

class ReportAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['title', 'price', 'type', 'created']
    list_filter = ['type', 'created']
    search_fields = ['title']
    actions = ["export_as_csv"]

admin.site.register(Report, ReportAdmin)