from django.urls import path
from .views import *

urlpatterns = [
    # Views
    path('', main, name='main'),
    path('graphic/', home, name='home'),
    path('events/', calendar_view, name='events'),
    path('kpi-view/', kpi_view, name='kpi-view'),
    path('report-view/', report_view, name='report-view'),
    path('export-report/', export_report_to_excel, name='export-report'),
    
    # Lists
    path('operator-list/', operator_list, name='operator-list'),
    path('teacher-list/', teacher_list, name='teacher-list'),
    path('pupil-list/', pupil_list, name='pupil-list'),
    path('lesson-list/<str:pk>/', lesson_list, name='lesson-list'),
    path('group-list/', group_list, name='group-list'),
    path('course-list/', course_list, name='course-list'),
    path('room-list/', room_list, name='room-list'),
    path('support-list/', support_list, name='support-list'),

    # Details
    path('group-detail/<str:pk>/', group_detail, name='group-detail'),
    path('course-detail/<str:pk>/', course_detail, name='course-detail'),
    path('lesson-detail/<str:pk>/', lesson_detail, name='lesson-detail'),
    path('room-detail/<str:pk>/', room_detail, name='room-detail'),

    # Create
    path('lesson-create/<str:pk>/', lesson_create, name='lesson-create'),

    # Update
    path('lesson-update/<str:pk>/', lesson_update, name='lesson-update'),
    path('group-update/<str:pk>/', group_update, name='group-update'),
    path('course-update/<str:pk>/', course_update, name='course-update'),
]