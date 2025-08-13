from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.crypto import get_random_string
import os
from academic.models import Department, Classroom  , Department
from home_auth.views import admin_required
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from school.views import create_notification


@admin_required
def add_teacher(request):
    if request.method == 'POST':
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        gender =  request.POST.get('gender')
        date_of_birth =  request.POST.get('date_of_birth')
        department = request.POST.get('department')
        mobile_number =  request.POST.get('mobile_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        teacher_image = request.FILES.get('teacher_image')
        department_obj = None
        if email:
            if CustomUser.objects.filter(email = email).exists():
                messages.warning(request, "Email already exists !")
                return redirect('add_teacher')
        if department:
            department_obj = Department.objects.get(id=department)
        user = CustomUser.objects.create(
            username = f'TCH{Teacher.objects.count()}',
            email = email,
            first_name=first_name,
            last_name=last_name,
            date_joined = timezone.now(),
        )
        raw_pass = get_random_string(10)
        user.set_password(raw_pass)
        user.save()
        user.groups.add(Group.objects.get(name='teachers'))
        ##Lưu thông tin
        teacher = Teacher.objects.create(
            user = user,
            gender =  gender,
            date_of_birth =  date_of_birth,
            mobile_number =  mobile_number,
            teacher_image = teacher_image,
            department = department_obj,
            address = address,
        )
        teacher.save()
        send_mail(
            f'Tạo tài khoản PRESKOOL thành công ',
            f'''Xin chào {user.first_name},
            Tài khoản của bạn đã được tạo thành công trên +hệ thống PRESKOOL vào lúc {user.date_joined.strftime('%y-%m-%d')} với tư cách giảng viên.
            Thông tin đăng nhập:
            - Tên đăng nhập: {user.username}
            - Mật khẩu: {raw_pass}
            Vui lòng đăng nhập và đổi mật khẩu tại PRESKOOL
            Trân trọng,  
            Ban quản trị hệ thống''',
            f'thereelduy@gmail.com',
            [user.email],
            fail_silently=False
        )
        create_notification(request.user, f'Add teacher: {teacher.user.first_name} {teacher.user.last_name}')
        messages.success(request, 'Teacher added successflly')
        # return render(request, 'teacher_list')
    department = Department.objects.all()
    classrooms = Classroom.objects.all()
    context = {
        'departments': department,
        'classrooms': classrooms,
    }
    return render(request,'teachers/add-teacher.html', context)

def teacher_list(request):
    teacher_list = Teacher.objects.all()
    context ={
        'teacher_list': teacher_list,
    }
    return render(request,'teachers/teachers.html', context)
@admin_required
def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    user = teacher.user if hasattr(teacher, 'user') else None
    department = Department.objects.all()
    classrooms = Classroom.objects.all()
    context = {
        'teacher': teacher,
        'departments': department,
        'classrooms': classrooms,
    }
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        teacher_image = request.FILES.get('teacher_image')
        department_obj = None
        if email:
            if CustomUser.objects.filter(email = email).exclude(id=teacher.user.id).exists():
                messages.warning(request, "Email already exist!")
                return redirect('edit_teacher', teacher.slug)
        if department:
            department_obj = Department.objects.get(id=department)
        if teacher_image:
            if teacher.teacher_image and os.path.isfile(teacher.teacher_image.path):
                os.remove(teacher.teacher_image.path)
            teacher.teacher_image = teacher_image

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        teacher.gender = gender
        teacher.date_of_birth = date_of_birth
        teacher.mobile_number = mobile_number
        teacher.address = address
        teacher.department = department_obj
        teacher.save()
        return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html', context)

def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug = slug)
    context ={
        'teacher': teacher
    }
    return render(request,'teachers/teacher-details.html', context)

@admin_required
def delete_teacher(request, slug):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, slug = slug)
        user = teacher.user
        user.delete()
        if teacher.teacher_image and os.path.isfile(teacher.teacher_image.path):
            os.remove(teacher.teacher_image.path)
        teacher.delete()
        create_notification(request.user, f' Deleted teacher: {teacher.user.first_name} {teacher.user.last_name }')
        return redirect('teacher_list')
    return HttpResponseForbidden()