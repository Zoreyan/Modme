from django.urls import path
from .views  import *

urlpatterns = [
    # Profiles
    path('pupil-profile/<str:pk>/', pupil_profile, name='pupil-profile'),
    path('teacher-profile/<str:pk>/', teacher_profile, name='teacher-profile'),
    path('operator-profile/<str:pk>/', operator_profile, name='operator-profile'),
    # List
    path('teacher-pupils/', teacher_pupils, name='teacher-pupils'),
    path('teacher-lessons/<str:pk>/', teacher_lessons, name='teacher-lessons'),
    path('teacher-groups/', teacher_groups, name='teacher-groups'),
    path('pupil-groups/', pupil_groups, name='pupil-groups'),
    path('pupil-lessons/<str:pk>/', pupil_lessons, name='pupil-lessons'),
    # Profile Login
    path('login/', login_page, name='login'),
    path('profile/<str:pk>/', profile, name='profile'),
    path('profile-access/<str:pk>/', profile_access, name='profile-access'),
    path('logout/', logout_user, name='logout'),
    # Other
    path('check-detail/<str:pk>/', check_detail, name='check-detail'),
    path('send-to-whatsapp/<str:pk>/', send_to_whatsapp, name='send-to-whatsapp'),
]