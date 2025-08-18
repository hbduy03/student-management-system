from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.crypto import get_random_string
import os
from academic.models import Department, Classroom, Major, SubjectDetail
from academic.views import admin_required, teacher_required
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from school.views import create_notification


# Create your views here.
@admin_required
def add_student(request):
    if request.method == 'POST':
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        gender =  request.POST.get('gender')
        date_of_birth =  request.POST.get('date_of_birth')
        student_class =  request.POST.get('student_class')
        major = request.POST.get('major')
        mobile_number =  request.POST.get('mobile_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        student_image = request.FILES.get('student_image')
        student_class_obj = None
        major_obj = None
        if email:
            if CustomUser.objects.filter(email = email).exists():
                messages.warning(request, "Email already exist!")
                return redirect('add_student')
        if student_class:
            student_class_obj = Classroom.objects.get(id=student_class)
        if major:
            major_obj = Major.objects.get(id=major)
        ## Nhận data gia đình từ forms
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        ##Lưu thông tin gia đình
        parent = Parent.objects.create(
            father_name = father_name,
            father_occupation = father_occupation,
            father_mobile = father_mobile,
            father_email = father_email,
            mother_name = mother_name,
            mother_occupation = mother_occupation,
            mother_mobile = mother_mobile,
            mother_email = mother_email,
            present_address = present_address,
            permanent_address = permanent_address
        )
        user = CustomUser.objects.create(
            username = f'STU{Student.objects.count()}',
            email = email,
            first_name=first_name,
            last_name=last_name,
            date_joined = timezone.now(),
        )
        raw_pass = get_random_string(10)
        user.set_password(raw_pass)
        user.save()
        user.groups.add(Group.objects.get(name='students'))
        ##Lưu thông tin
        student = Student.objects.create(
            user = user,
            gender =  gender,
            date_of_birth =  date_of_birth,
            student_class =  student_class_obj,
            mobile_number =  mobile_number,
            student_image = student_image,
            parent = parent,
            major = major_obj,
            address = address,
        )
        send_mail(
            f'Tạo tài khoản PRESKOOL thành công ',
            f'''Xin chào {user.first_name},
            Tài khoản của bạn đã được tạo thành công trên +hệ thống PRESKOOL vào lúc {user.date_joined.strftime('%y-%m-%d')} với tư cách sinh viên.
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
        create_notification(request.user, f'Add student: {student.user.first_name} {student.user.last_name}')
        messages.success(request, 'Student added successflly')
        # return render(request, 'student_list')
    major = Major.objects.all()
    classrooms = Classroom.objects.all()
    context = {
        'majors': major,
        'classrooms': classrooms,
    }
    return render(request,'students/add-student.html', context)

@admin_required
def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    context ={
        'student_list': student_list,
    }
    return render(request,'students/students.html', context)

@admin_required
def edit_student(request, slug):
    student = get_object_or_404(Student, slug =slug)
    parent = student.parent if hasattr(student, 'parent') else None
    user = student.user if hasattr(student, 'user') else None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        major = request.POST.get('major')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        student_image = request.FILES.get('student_image')
        student_class_obj = None
        major_obj = None
        if email:
            if CustomUser.objects.filter(email = email).exclude(id=student.user.id).exists():
                messages.warning(request, "Email already exist!")
                return redirect('edit_student', student.slug)
        if student_class:
            student_class_obj = Classroom.objects.get(id=student_class)
        if major:
            major_obj = Major.objects.get(id=major)
        if student_image:
            if student.student_image and os.path.isfile(student.student_image.path):
                os.remove(student.student_image.path)
            student.student_image = student_image
        ## Nhận data gia đình từ forms
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

        user.email = email
        user.first_name =  first_name
        user.last_name =  last_name
        user.save()

        student.gender =  gender
        student.date_of_birth =  date_of_birth
        student.mobile_number = mobile_number
        student.address = address
        student.major = major_obj
        student.student_class = student_class_obj
        student.save()
        return redirect('student_list')
    major = Major.objects.all()
    classrooms = Classroom.objects.all()
    context = {
        'student': student,
        'parent': parent,
        'majors': major,
        'classrooms': classrooms,
    }
    return render(request,'students/edit-student.html', context)

def view_student(request, slug):
    student = get_object_or_404(Student, slug = slug)
    scores = SubjectDetail.objects.filter(student=student).select_related('subject')
    context ={
        'student': student,
        'scores': scores
    }

    return render(request,'students/student-details.html', context)

@admin_required
def delete_student(request, slug):
    if request.method == 'POST':
        student = get_object_or_404(Student, slug = slug)
        user = student.user
        user.delete()
        parent = student.parent
        parent.delete()
        if student.student_image and os.path.isfile(student.student_image.path):
            os.remove(student.student_image.path)
        student.delete()
        create_notification(request.user, f' Deleted student: {student.user.first_name} {student.user.last_name }')
        return redirect('student_list')
    return HttpResponseForbidden()