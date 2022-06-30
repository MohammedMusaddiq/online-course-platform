from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('', views.StudentDashboard.as_view(), name='student-dashboard'),
    path('explore/', views.CourseList.as_view(), name='student-explore'),
    path('subscribe/', views.course_subscribe, name='subscribe'),
    path('my-courses/', views.SubscribedCourses.as_view(), name='my-courses'),
    path('unsubscribe/', views.unsubscribe, name='un-subscribe'),
    path('search/', views.SearchCourse.as_view(), name='search'),
]
