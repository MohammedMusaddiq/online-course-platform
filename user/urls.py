from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('student-login/', views.StudentLoginView.as_view(), name='student-login'),
    path('student-register/', views.StudentRegisterView.as_view(), name='student-register'),
    path('verify-otp/<email>', views.VerifyOtp.as_view(), name='verify-otp'),
    path('teacher-login/', views.TeacherLoginView.as_view(), name='teacher-login'),
    path('teacher-register/', views.TeacherRegisterView.as_view(), name='teacher-register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
