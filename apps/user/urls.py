from django.urls import path
from .views  import *

urlpatterns = [
    path('pupil-profile/<str:pk>/', pupil_profile, name='pupil-profile'),
    path('teacher-profile/<str:pk>/', teacher_profile, name='teacher-profile'),
    path('teacher-pupils/', teacher_pupils, name='teacher-pupils'),
    path('teacher-lessons/', teacher_lessons, name='teacher-lessons'),
    path('pupil-lessons/', pupil_lessons, name='pupil-lessons'),
    path('login/', login_page, name='login'),
    path('profile/<str:pk>/', profile, name='profile'),
    path('check-detail/<str:pk>/', check_detail, name='check-detail'),
    path('profile-access/<str:pk>/', profile_access, name='profile-access'),
    path('logout/', logout_user, name='logout'),
]