from django.conf import settings
from django.db import models
from teacher.models import Course

User = settings.AUTH_USER_MODEL


class CourseRegistration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    subscribed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Course Registrations'

    def __str__(self):
        return f"{self.course.course_name}"
