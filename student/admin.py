from django.contrib import admin
from .models import CourseRegistration


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'subscribed', 'paid']
