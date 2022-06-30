from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    published_date = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ['-published_date']

    def __str__(self):
        return self.course_name


class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
