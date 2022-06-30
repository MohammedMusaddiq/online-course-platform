from django.contrib import admin

from .models import (
    Course,
    Content,
)


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ['instructor', 'course_name', 'published_date', 'updated_on']
