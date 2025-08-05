from django.shortcuts import render
from django.contrib import messages

from academic.models import Department
from school.views import create_notification
from teacher.models import Teacher


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