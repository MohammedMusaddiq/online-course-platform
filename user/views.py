from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .email import send_otp_via_mail
from django.views.generic.base import TemplateView

User = get_user_model()


def welcome_page(request):
    context = {
        'title': 'DA | Welcome'
    }
    if request.user.is_authenticated:
        u = User.objects.get(id=request.user.id)
        if u.is_student:
            return redirect('student:student-dashboard')
        elif u.is_teacher:
            return redirect('teacher:teachers-dashboard')
        else:
            return render(request, 'user/welcome.html', context)

    return render(request, 'user/welcome.html', context)


class StudentLoginView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            u = User.objects.get(id=self.request.user.id)
            if u.is_student:
                return redirect('student:student-dashboard')
        return render(self.request, 'user/student-login.html', {'title': 'DA-Student | Login'})

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user_obj = authenticate(username=email, password=password)
        if user_obj is None:
            messages.error(self.request, "Wrong Credentials. Please Try Again")
            return render(self.request, 'user/student-login.html', {'title': 'DA-Student | Login'})
        elif user_obj.is_student and user_obj.is_verified:
            login(self.request, user_obj)
            messages.success(self.request, f"Logged in Successfully as {self.request.user.first_name}")
            return redirect('student:student-dashboard')
        messages.error(self.request, "Account Not Verified | please verify your account first")
        return redirect('user:verify-otp', email)


class StudentRegisterView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            u = User.objects.get(id=self.request.user.id)
            if u.is_student:
                return redirect('student:student-dashboard')
        return render(self.request, 'user/student-register.html', {'title': 'DA-Student | Register'})

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        if User.objects.filter(email=email).exists():
            messages.error(self.request, "Email Already Exists. Please Try Again")
            return redirect('user:student-register')
        else:
            try:
                user_obj = User.objects.create_user(
                    email=email,
                    password=password,
                )
                user_obj.first_name = first_name
                user_obj.last_name = last_name
                user_obj.is_student = True
                user_obj.save()
                send_otp_via_mail(email)
                messages.success(self.request, "Verify with otp sent to your email to complete signup")
                return redirect('user:verify-otp', email=email)
            except Exception as e:
                print(e)
                messages.error(self.request, "Unknown Error..Please Try Again")
                return redirect('user:student-register')


class TeacherLoginView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            u = User.objects.get(id=self.request.user.id)
            if u.is_teacher:
                return redirect('teacher:teachers-dashboard')
        return render(self.request, 'user/teacher-login.html', {'title': 'DA-Teacher | Login'})

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user_obj = authenticate(username=email, password=password)
        if user_obj is None:
            messages.error(self.request, "Wrong Credentials. Please Try Again")
            return redirect('user:teacher-login')
        elif user_obj.is_teacher and user_obj.is_verified:
            login(self.request, user_obj)
            messages.success(self.request, f"Logged in successfully as {self.request.user.first_name}")
            return redirect('teacher:teachers-dashboard')
        messages.error(self.request, "Permission Error. Not a Teacher Account")
        return redirect('user:verify-otp', email)


class TeacherRegisterView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            u = User.objects.get(id=self.request.user.id)
            if u.is_teacher:
                return redirect('teacher:teachers-dashboard')
        return render(self.request, 'user/teacher-register.html', {'title': 'DA-Teacher | Register'})

    def post(self, *args, **kwargs):
        print('post')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        if User.objects.filter(email=email).exists():
            messages.error(self.request, "Email Already Exists. Please Try Again")
            return redirect('user:teacher-register')
        else:
            try:
                user_obj = User.objects.create_user(
                    email=email,
                    password=password,
                )
                user_obj.first_name = first_name
                user_obj.last_name = last_name
                user_obj.is_teacher = True
                user_obj.save()
                send_otp_via_mail(email)
                messages.success(self.request, "Verify with otp sent to your email to complete signup")
                return redirect('user:verify-otp', email)
            except Exception as e:
                print(e)
                messages.error(self.request, "Unknown Error..Please Try Again")
                return redirect('user:teacher-register', )


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return HttpResponseRedirect('/')


class VerifyOtp(View):
    @staticmethod
    def get(request, *args, **kwargs):
        email = kwargs.get('email')
        return render(request, 'user/verify_otp.html', {'title': 'DA-Teacher | Verify OTP', 'email': email})

    @staticmethod
    def post(request, *args, **kwargs):
        email = kwargs.get('email')
        otp = request.POST.get('otp')
        user_obj = User.objects.get(email=email)
        if int(user_obj.otp) == int(otp):
            user_obj.is_verified = True
            user_obj.save()
            messages.success(request, "Verified Successfully. Please Login to Continue")
            return redirect('user:student-login')
        else:
            messages.error(request, "Wrong OTP. Please Try Again")
            return redirect('user:verify-otp', email=email)
