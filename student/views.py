from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.core import serializers
from django.views.generic import TemplateView, ListView
from teacher.models import Course
from .models import CourseRegistration

User = get_user_model()


class StudentDashboard(TemplateView):
    template_name = 'student/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"DA | {self.request.user}"
        context['navbar'] = "student-dashboard"
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


class CourseList(ListView):
    paginate_by = 8
    model = Course
    template_name = 'student/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Courses | {self.request.user.first_name}"
        context['navbar'] = "student-explore"
        return context


def course_subscribe(request):
    c_id = request.GET.get('id')
    c = Course.objects.get(id=c_id)
    cr = CourseRegistration.objects.filter(student=request.user)
    data = {}
    if cr.filter(course_id=c_id).exists():
        data['message'] = "Already Subscribed to Course"
        data['color'] = "alert-danger"

    else:
        CourseRegistration.objects.create(
            student=request.user,
            course=c,
            subscribed=True
        )
        data['message'] = "Successfully Subscribed to course. Go to you Course Section"
        data['color'] = "alert-success"
    return JsonResponse(data)


class SubscribedCourses(ListView):
    template_name = 'student/my-courses.html'
    paginate_by = 8

    def get_queryset(self):
        return CourseRegistration.objects.filter(student=self.request.user, subscribed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"My Courses | {self.request.user.first_name}"
        context['navbar'] = "student-courses"
        return context


def unsubscribe(request):
    if request.method == 'GET':
        idx = request.GET.get('idx')
        crd = CourseRegistration.objects.get(id=idx)
        crd.delete()
        return JsonResponse({"data": idx})


class SearchCourse(ListView):
    paginate_by = 8
    model = Course
    template_name = 'student/explore.html'

    def get_queryset(self):
        return Course.objects.filter(course_name__icontains=self.request.GET.get('query'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Courses | {self.request.user.first_name}"
        context['navbar'] = "student-explore"
        return context
