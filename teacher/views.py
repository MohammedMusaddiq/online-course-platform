from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from .models import Course, Content
from student.models import CourseRegistration
from paypal.standard.forms import PayPalPaymentsForm
import random

User = get_user_model()


class TeacherDashboard(TemplateView):
    template_name = 'teacher/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"DA | {self.request.user.first_name}"
        context['navbar'] = "teacher-dashboard"
        return context


class CoursesList(ListView):
    template_name = 'teacher/courses.html'
    model = Course

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"DA | {self.request.user.first_name}"
        context['navbar'] = "teacher-courses"
        return context


class CourseCreate(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'teacher/add-courses.html',
                      {'title': f'DA | {self.request.user.first_name}', 'navbar': 'teacher-courses'})

    def post(self, request, *args, **kwargs):
        course_title = request.POST.get('course-title')
        price = request.POST.get('price')
        try:
            c = Course.objects.create(
                instructor=request.user,
                course_name=course_title,
                price=price,
            ).save()
            messages.success(request, "Course created successfully")
            return redirect('teacher:teachers-courses')
        except Exception as e:
            messages.error(request, "Something went wrong. Try again")
            print(e)
            return redirect('teacher:create-courses')


def delete_content(request, pk):
    obj = Content.objects.get(id=pk)
    obj.delete()
    return redirect('teacher:teachers-courses')


def edit_content(request, pk):
    c = Content.objects.get(id=pk)
    if request.method == 'POST':
        cname = request.POST.get('course-title')
        desc = request.POST.get('course-description')
        content = request.POST.get('content')
        c.course.instructor = request.user
        c.course_name = cname
        c.topic = desc
        c.content = content
        c.save()
        messages.success(request, "Updated the Selected Course")
        return redirect('teacher:teachers-courses')
    context = {
        'course': c,
        'title': f'DA | {request.user.first_name}',
        'navbar': 'teacher-courses'
    }
    return render(request, 'teacher/edit-course.html', context)


class StudentList(ListView):
    template_name = 'teacher/students.html'
    paginate_by = 8

    def get_queryset(self):
        return CourseRegistration.objects.filter(course__instructor=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"DA | {self.request.user.first_name}"
        context['navbar'] = "teacher-students"
        return context


def add_topic(request, pk):
    if request.method == 'GET':
        course = Course.objects.get(id=pk)
        context = {
            'course': course,
            'title': f'DA | {request.user.first_name}',
            'navbar': 'teacher-courses'
        }
        return render(request, 'teacher/add-topics.html', context)
    else:
        course = Course.objects.get(id=pk)
        topic = request.POST.get('topic')
        content = request.POST.get('content')
        try:
            c = Content.objects.create(
                course=course,
                topic=topic,
                content=content,
            ).save()
            messages.success(request, "Topic added successfully")
            return redirect('teacher:teachers-courses')
        except Exception as e:
            messages.error(request, "Something went wrong. Try again")
            print(e)
            return redirect('teacher:teachers-courses')


def delete_course(request, pk):
    obj = Course.objects.get(id=pk)
    obj.delete()
    return redirect('teacher:teachers-courses')


def confirm_order(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        cr = CourseRegistration.objects.create(
            course=course,
            student=request.user,
        )
        request.session['registration'] = cr.id
        return redirect('teacher:process_payment')
    context = {
        'title': f'DA | {request.user}',
        'navbar': 'teacher-courses',
        'course': course,
    }
    return render(request, 'student/order-confirm.html', context)


def process_payment(request):
    cr_id = request.session.get('registration')
    cr = CourseRegistration.objects.get(id=cr_id)
    paypal_dict = {'business': settings.PAYPAL_RECEIVER_EMAIL,
                   'amount': str(cr.course.price),
                   'item_name': str(f'Order- {cr.course.course_name}'),
                   'invoice': str(cr.id),
                   'currency_code': 'USD',
                   'notify_url': f"http://{request.get_host()}{reverse('paypal-ipn')}",
                   'return_url': f"http://{request.get_host()}{reverse('teacher:payment_done')}",
                   'cancel_return': f"http://{request.get_host()}{reverse('teacher:payment_cancelled')}"}

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'title': f'DA | {request.user}',
        'navbar': 'teacher-courses',
        'form': form,
    }
    return render(request, 'student/pay.html', context)


@csrf_exempt
def payment_done(request):
    return render(request, 'student/payment-success.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'student/payment-failed.html')
