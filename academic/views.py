from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from academic.models import Department, Major
from school.views import create_notification
from teacher.models import Teacher

# ---------- CRUD Department Object ----------

def add_department(request):
    teacher = Teacher.objects.all()
    context = {
       'teachers': teacher
    }
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        name = request.POST.get('name')
        header = request.POST.get('hod')
        hod = None
        if header:
            hod = Teacher.objects.get(id=header)
            if Department.objects.filter(hod=hod).exists():
                messages.error(request, f'"{hod.user.first_name}" đã lả trưởng nhóm khoa khác.')
                return render(request, 'departments/add-department.html', context)
        if Department.objects.filter(department_id=department_id).exists():
            messages.error(request, f'"{department_id}" đã tồn tại')
            return render(request, 'departments/add-department.html', context)
        department = Department.objects.create(
        department_id = department_id,
        name = name,
        hod = hod,
        )
        create_notification(request.user, f'Add department: {department.name}')
        messages.success(request, 'Department added successfully')
    return render(request,'departments/add-department.html', context)

def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    teacher = Teacher.objects.all()
    context = {
       'teachers': teacher,
        'department' :department,
    }
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        name = request.POST.get('name')
        header = request.POST.get('hod')
        hod = None
        if header:
            hod = Teacher.objects.get(id=header)
            if Department.objects.filter(hod=hod).exclude(id=department.id).exists():
                messages.error(request, f'"{hod.user.first_name}" đã lả trưởng nhóm khoa khác.')
                return render(request, 'departments/edit-department.html', context)
        if Department.objects.filter(department_id=department_id).exclude(id=department.id).exists():
            messages.error(request, f'"{department_id}" đã tồn tại')
            return render(request, 'departments/edit-department.html', context)
        department.department_id = department_id
        department.name = name
        department.hod = hod
        department.save()
        return redirect('department_list')
    return render(request, 'departments/edit-department.html', context)

def department_list(request):
    department_list = Department.objects.all()
    context ={
        'department_list': department_list,
    }
    return render(request,'departments/departments.html', context)

def delete_department(request, id):
    if request.method == 'POST':
        department = get_object_or_404(Department, id = id)
        department.delete()
        create_notification(request.user, f' Deleted department: {department.department_id}')
        return redirect('department_list')
    return HttpResponseForbidden()

# ---------- CRUD Major Object ----------

def add_major(request):
    department = Department.objects.all()
    context = {
       'departments': department
    }
    if request.method == 'POST':
        major_id = request.POST.get('major_id')
        name = request.POST.get('name')
        department = request.POST.get('department')
        department_obj = None
        if department:
            department_obj = Department.objects.get(id=department)
        if Major.objects.filter(major_id=major_id).exists():
            messages.error(request, f'"{major_id}" đã tồn tại')
            return render(request, 'majors/add-major.html', context)
        major = Major.objects.create(
        major_id = major_id,
        name = name,
        department = department_obj,
        )
        create_notification(request.user, f'Add major: {major.name}')
        messages.success(request, 'major added successfully')
    return render(request,'majors/add-major.html', context)

def major_list(request):
    major_list = Major.objects.all()
    context ={
        'major_list': major_list,
    }
    return render(request,'majors/majors.html', context)

def edit_major(request, id):
    major = get_object_or_404(Major, id=id)
    department = Department.objects.all()
    context = {
       'major': major,
        'departments' : department,
    }
    if request.method == 'POST':
        major_id = request.POST.get('major_id')
        name = request.POST.get('name')
        department = request.POST.get('department')
        department_obj = None
        if department:
            department_obj = Department.objects.get(id=department)
        if Major.objects.filter(major_id=major_id).exclude(id=major.id).exists():
            messages.error(request, f'"{major_id}" đã tồn tại')
            return render(request, 'majors/edit-major.html', context)
        major.major_id = major_id
        major.name = name
        major.department = department_obj
        major.save()
        return redirect('major_list')
    return render(request, 'majors/edit-major.html', context)

def delete_major(request, id):
    if request.method == 'POST':
        major = get_object_or_404(Major, id = id)
        major.delete()
        create_notification(request.user, f' Deleted major: {major.major_id}')
        return redirect('major_list')
    return HttpResponseForbidden()