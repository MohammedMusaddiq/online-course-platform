from django.urls import path

from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.TeacherDashboard.as_view(), name='teachers-dashboard'),
    path('courses/', views.CoursesList.as_view(), name='teachers-courses'),
    path('add-courses/', views.CourseCreate.as_view(), name='create-courses'),
    path('<int:pk>/delete/', views.delete_content, name='delete-content'),
    path('<int:pk>/delete/courses/', views.delete_course, name='delete-course'),
    path('<int:pk>/edit/', views.edit_content, name='edit-content'),
    path('<int:pk>/add-topic/', views.add_topic, name='add_topic'),
    path('student-list/', views.StudentList.as_view(), name='student-list'),
    path('confirm-order/<int:pk>/', views.confirm_order, name='confirm-order'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]
