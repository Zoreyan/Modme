from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('teacher-list/', teacher_list, name='teacher-list'),
    path('pupil-list/', pupil_list, name='pupil-list'),
    path('lesson-list/<str:pk>/', lesson_list, name='lesson-list'),
    path('group-list/', group_list, name='group-list'),
    path('group-detail/<str:pk>/', group_detail, name='group-detail'),
    path('group-update/<str:pk>/', group_update, name='group-update'),
    path('room-list/', room_list, name='room-list'),
    path('course-list/', course_list, name='course-list'),
    path('course-detail/<str:pk>/', course_detail, name='course-detail'),
    path('lesson-detail/<str:pk>/', lesson_detail, name='lesson-detail'),
    path('lesson-create/<str:pk>/', lesson_create, name='lesson-create'),
    path('lesson-update/<str:pk>/', lesson_update, name='lesson-update'),
    path('events/', calendar_view, name='events'),
    path('report-view/', report_view, name='report-view'),
    path('kpi-view/', kpi_view, name='kpi-view'),
]