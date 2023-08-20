from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(WeekDays)

admin.site.register(Course)
admin.site.register(Room)