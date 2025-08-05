from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import PasswordResetRequest, CustomUser
from django.utils.crypto import get_random_string

# Hàm cho phép User tạo tài khoản, nhưng đã chuyển sang mô hình admin quản lý tạo tài khoản
# def signup_views(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         role = request.POST.get('role', 'student')
#
#         user = CustomUser.objects.create_user(
#             username=email,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password
#         )
#         if role == 'student':
#             user.is_student = True
#         elif role == 'teacher':
#             user.is_teacher = True
#         elif role == 'admin':
#             user.is_teacher = True
#
#         user.save()
#         login(request, user)
#         messages.success(request, 'Sign up checked')
#         return redirect('index')
#     return render(request,'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login sucecss')

            if user.groups.filter(name='admins').exists():
                return redirect ('admin_dashboard')
            elif user.groups.filter(name='teachers').exists():
                return redirect ('teacher_dashboard')
            elif user.groups.filter(name='students').exists():
                return redirect ('dashboard')
            else:
                messages.error(request, 'Inaled user role')
                return redirect('index')
        else:
            messages.error(request ,'inlvaed Cesles')
    return render (request, 'authentication/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = CustomUser.objects.filter(email = email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email = email, token = token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to email')
        else:
            messages.error(request, 'Email not found')
    return render (request, 'authentication/forgot-password.html')

def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token = token).first()
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link  l')
        return redirect('index')
    if request.method == 'POST':

        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reseted')
        return redirect('login')
    return render(request, 'authentication/reset_password.html', {'token': token})

def logout_view(request):
    logout(request)
    messages.success(request,'Logout ')
    return redirect('index')
