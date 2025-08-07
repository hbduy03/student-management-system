from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib import messages

from school.views import create_notification


# Create your views here.
def add_teacher(request):
    if request.method == 'POST':
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        gender =  request.POST.get('gender')
        date_of_birth =  request.POST.get('date_of_birth')
        joining_date =  request.POST.get('joining_date')
        mobile_number =  request.POST.get('mobile_number')
        admission_number =  request.POST.get('admission_number')
        section =  request.POST.get('section')
        teacher_image = request.FILES.get('teacher_image')
        #LẤy Object Classroom
        classr = request.POST.get('teacher_class')
        teacher_class = Classroom.objects.get(classr)
        teacher = Teacher.objects.create(
            first_name =  first_name,
            last_name =  last_name,
            teacher_id =  teacher_id,
            gender =  gender,
            date_of_birth =  date_of_birth,
            teacher_class =  teacher_class,
            religion =  religion,
            joining_date =  joining_date,
            mobile_number =  mobile_number,
            admission_number =  admission_number,
            section =  section,
            teacher_image = teacher_image,
        )
        create_notification(request.user, f'Add teacher: {teacher.user.first_name} {teacher.user.last_name}')
        messages.success(request, 'teacher added succesflly')
        # return render(request, 'teacher_list')
    return render(request,'teachers/add-teacher.html')

def teacher_list(request):
    teacher_list = Teacher.objects.select_related('parent').all()
    unread_notification = request.user.notification_set.filter(is_read=False)
    context ={
        'teacher_list': teacher_list,
        'unread_notification': unread_notification
    }

    return render(request,'teachers/teachers.html', context)

def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug =slug)
    if request.method == 'POST':
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        teacher_id =  request.POST.get('teacher_id')
        gender =  request.POST.get('gender')
        date_of_birth =  request.POST.get('date_of_birth')
        teacher_class =  request.POST.get('teacher_class')
        religion =  request.POST.get('religion')
        joining_date =  request.POST.get('joining_date')
        mobile_number =  request.POST.get('mobile_number')
        admission_number =  request.POST.get('admission_number')
        section =  request.POST.get('section')
        teacher_image = request.FILES.get('teacher_image')

        teacher.first_name =  first_name,
        teacher.last_name =  last_name,
        teacher.teacher_id =  teacher_id,
        teacher.gender =  gender,
        teacher.date_of_birth =  date_of_birth,
        teacher.teacher_class =  teacher_class,
        teacher.religion =  religion,
        teacher.joining_date =  joining_date,
        teacher.mobile_number =  mobile_number,
        teacher.admission_number =  admission_number,
        teacher.section =  section,
        teacher.teacher_image = teacher_image,
        teacher.save()
        return render(request,'teacher_list')
    context = {
        'teacher': teacher,
    }
    return render(request,'teachers/edit-teacher.html', context)

def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, teacher_id = slug)
    context ={
        'teacher': teacher
    }
    return render(request,'teachers/teacher-details.html', context)

def delete_teacher(request, slug):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, slug = slug)
        teacher_name = f'{ teacher.first_name} {teacher.last_name}'
        teacher.delete()
        create_notification(request.user, f' Deleted teacher: {teacher.first_name} {teacher_name }')
        return redirect('teacher_list')
    return HttpResponseForbidden()