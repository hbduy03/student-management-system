from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from academic.models import Department, Subject, Major, Classroom, ClassSection, SubjectDetail
from home_auth.views import admin_required, teacher_required
from school.views import create_notification
from student.models import Student
from teacher.models import Teacher
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden

# ---------- CRUD Department Object ----------
@admin_required
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
                messages.warning(request, f'"{hod.user.first_name}" đã lả trưởng nhóm khoa khác.')
                return render(request, 'departments/add-department.html', context)
        if Department.objects.filter(department_id=department_id).exists():
            messages.warning(request, f'"{department_id}" đã tồn tại')
            return render(request, 'departments/add-department.html', context)
        department = Department.objects.create(
        department_id = department_id,
        name = name,
        hod = hod,
        )
        create_notification(request.user, f'Add department: {department.name}')
        messages.success(request, 'Department added successfully')
    return render(request,'departments/add-department.html', context)

@admin_required
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
                messages.warning(request, f'"{hod.user.first_name}" đã lả trưởng nhóm khoa khác.')
                return render(request, 'departments/edit-department.html', context)
        if Department.objects.filter(department_id=department_id).exclude(id=department.id).exists():
            messages.warning(request, f'"{department_id}" đã tồn tại')
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

@admin_required
def delete_department(request, id):
    if request.method == 'POST':
        department = get_object_or_404(Department, id = id)
        department.delete()
        create_notification(request.user, f' Deleted department: {department.department_id}')
        return redirect('department_list')
    return HttpResponseForbidden()

# ---------- CRUD Major Object ----------

@admin_required
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
            messages.warning(request, f'"{major_id}" đã tồn tại')
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

@admin_required
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
            messages.warning(request, f'"{major_id}" đã tồn tại')
            return render(request, 'majors/edit-major.html', context)
        major.major_id = major_id
        major.name = name
        major.department = department_obj
        major.save()
        return redirect('major_list')
    return render(request, 'majors/edit-major.html', context)

@admin_required
def delete_major(request, id):
    if request.method == 'POST':
        major = get_object_or_404(Subject, id = id)
        major.delete()
        create_notification(request.user, f' Deleted major: {major.major_id}')
        return redirect('major_list')
    return HttpResponseForbidden()

# ---------- CRUD Subject Object ----------

@admin_required
def add_subject(request):
    major = Major.objects.all()
    context = {
       'majors': major
    }
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        name = request.POST.get('name')
        attribute = request.POST.get('attribute')
        major = request.POST.get('major')
        major_obj = None
        if major:
            major_obj = Major.objects.get(id=major)
        if Subject.objects.filter(subject_id=subject_id).exists():
            messages.warning(request, f'"{subject_id}" đã tồn tại')
            return render(request, 'subjects/add-subject.html', context)
        subject = Subject.objects.create(
        subject_id = subject_id,
        name = name,
        attribute = attribute,
        major = major_obj,
        )
        create_notification(request.user, f'Add subject: {subject.name}')
        messages.success(request, 'subject added successfully')
    return render(request,'subjects/add-subject.html', context)

def subject_list(request):
    subject_list = Subject.objects.all()
    context ={
        'subject_list': subject_list,
    }
    return render(request,'subjects/subjects.html', context)

@admin_required
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    major = Major.objects.all()
    context = {
       'subject': subject,
        'majors' : major,
    }
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        name = request.POST.get('name')
        attribute = request.POST.get('attribute')
        major = request.POST.get('major')
        major_obj = None
        if major:
            major_obj = Major.objects.get(id=major)
        if Subject.objects.filter(subject_id=subject_id).exclude(id=subject.id).exists():
            messages.warning(request, f'"{subject_id}" đã tồn tại')
            return render(request, 'subjects/edit-subject.html', context)
        subject.subject_id = subject_id
        subject.name = name
        subject.attribute = attribute
        subject.major = major_obj
        subject.save()
        return redirect('subject_list')
    return render(request, 'subjects/edit-subject.html', context)

@admin_required
def delete_subject(request, id):
    if request.method == 'POST':
        subject = get_object_or_404(Subject, id = id)
        subject.delete()
        create_notification(request.user, f' Deleted subject: {subject.subject_id}')
        return redirect('subject_list')
    return HttpResponseForbidden()

# ---------- CRUD Classroom Object ----------

@admin_required
def add_classroom(request):
    teacher = Teacher.objects.all()
    context = {
       'teachers': teacher
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher = request.POST.get('home_teacher')
        capacity = request.POST.get('capacity')
        teacher_obj = None
        if teacher:
            teacher_obj = Teacher.objects.get(id=teacher)
        if Classroom.objects.filter(name=name).exists():
            messages.warning(request, f'"{name}" đã tồn tại')
            return render(request, 'classrooms/add-classroom.html', context)
        classroom = Classroom.objects.create(
        name = name,
        capacity = capacity,
        home_teacher = teacher_obj,
        )
        create_notification(request.user, f'Add classroom: {classroom.name}')
        messages.success(request, 'classroom added successfully')
    return render(request,'classrooms/add-classroom.html', context)

def classroom_list(request):
    classroom_list = Classroom.objects.all()
    context ={
        'classroom_list': classroom_list,
    }
    return render(request,'classrooms/classrooms.html', context)

@admin_required
def edit_classroom(request, id):
    classroom = get_object_or_404(Classroom, id=id)
    teacher = Teacher.objects.all()
    context = {
       'classroom': classroom,
        'teachers' : teacher,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher = request.POST.get('home_teacher')
        capacity = request.POST.get('capacity')
        teacher_obj = None
        if teacher:
            teacher_obj = Teacher.objects.get(id=teacher)
        if Classroom.objects.filter(name=name).exclude(id=classroom.id).exists():
            messages.warning(request, f'"{name}" đã tồn tại')
            return render(request, 'classrooms/edit-classroom.html', context)
        classroom.name = name
        classroom.capacity = capacity
        classroom.home_teacher = teacher_obj
        classroom.save()
        return redirect('classroom_list')
    return render(request, 'classrooms/edit-classroom.html', context)

@admin_required
def delete_classroom(request, id):
    if request.method == 'POST':
        classroom = get_object_or_404(Classroom, id = id)
        classroom.delete()
        create_notification(request.user, f' Deleted classroom: {classroom.name}')
        return redirect('classroom_list')
    return HttpResponseForbidden()

# ---------- CRUD ClassSection Object ----------
@admin_required
def add_section(request):
    teacher = Teacher.objects.all()
    classroom = Classroom.objects.all()
    subject = Subject.objects.all()
    context = {
       'teachers': teacher,
        'classrooms': classroom,
        'subjects': subject,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        classroom = request.POST.get('classroom')
        teacher = request.POST.get('teacher')
        subject = request.POST.get('subject')
        capacity = request.POST.get('capacity')
        classroom_obj = None
        teacher_obj = None
        subject_obj = None
        if classroom:
            classroom_obj = Classroom.objects.get(id=classroom)
        if teacher:
            teacher_obj = Teacher.objects.get(id=teacher)
        if subject:
            subject_obj = Subject.objects.get(id=subject)
        if ClassSection.objects.filter(name=name).exists():
            messages.warning(request, f'"{name}" đã tồn tại')
            return render(request, 'classsections/add-classsection.html', context)
        classsection = ClassSection.objects.create(
            name = name,
            classroom = classroom_obj,
            teacher = teacher_obj,
            subject = subject_obj,
            capacity = capacity
        )
        create_notification(request.user, f'Add classsection: {classsection.id}')
        messages.success(request, 'classsection added successfully')
    return render(request,'classsections/add-classsection.html', context)

def section_list(request):
    section_list = ClassSection.objects.all()
    context ={
        'section_list': section_list,
    }
    return render(request,'classsections/classsections.html', context)

@admin_required
def edit_section(request, id):
    section = get_object_or_404(ClassSection, id=id)
    teacher = Teacher.objects.all()
    classroom = Classroom.objects.all()
    subject = Subject.objects.all()
    context = {
       'classsection': section,
        'classrooms': classroom,
        'teachers' : teacher,
        'subjects' : subject
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        classroom = request.POST.get('classroom')
        teacher = request.POST.get('teacher')
        subject = request.POST.get('subject')
        capacity = request.POST.get('capacity')
        classroom_obj = None
        teacher_obj = None
        subject_obj = None
        if classroom:
            classroom_obj = Classroom.objects.get(id=classroom)
        else:
            messages.warning(request, f'"Classroom không dược để trống')
            return render(request, 'classsections/edit-classsection.html', context)
        if teacher:
            teacher_obj = Teacher.objects.get(id=teacher)
        if subject:
            subject_obj = Subject.objects.get(id=subject)
        if ClassSection.objects.filter(name=name).exclude(id=section.id).exists():
            messages.warning(request, f'"{name}" đã tồn tại')
            return render(request, 'classsections/edit-classsection.html', context)
        section.name = name
        section.classroom = classroom_obj
        section.teacher = teacher_obj
        section.subject = subject_obj
        section.capacity = capacity
        section.save()
        return redirect('section_list')
    return render(request, 'classsections/edit-classsection.html', context)

@admin_required
def delete_section(request, id):
    if request.method == 'POST':
        section = get_object_or_404(ClassSection, id = id)
        section.delete()
        create_notification(request.user, f' Deleted section: {section.name }')
        return redirect('section_list')
    return HttpResponseForbidden()

def view_section(request, id):
    section = get_object_or_404(ClassSection, id= id)
    subjects = SubjectDetail.objects.filter(
        subject=section.subject,
        student__in=section.students.all()
    ).select_related('student__user')
    context = {
        'section': section,
        'subjects': subjects,
    }
    return render(request, 'classsections/classsection-detail.html', context)

@admin_required
def add_student_section(request, id):
    section = get_object_or_404(ClassSection, id= id)
    students = Student.objects.all()
    current_ids = section.students.values_list('id', flat=True)
    context = {
        'section': section,
        'students': students,
        'current_ids': current_ids,
    }
    if request.method == 'POST':
        selected_ids = request.POST.getlist('students')  # danh sách được check
        selected_ids = set(map(int, selected_ids))

        # Xóa những sinh viên bị bỏ check
        for student_id in current_ids:
            if student_id not in selected_ids:
                section.students.remove(student_id)

        # Thêm những sinh viên được check mới
        for student_id in selected_ids:
            if student_id not in current_ids:
                section.students.add(student_id)

        return redirect('view_section', id= section.id)
    return render(request, 'classsections/add-student-section.html', context)

@teacher_required
def enter_scores(request, section_id):
    section = get_object_or_404(ClassSection, pk=section_id)
    students = section.students.all()  # Quan hệ ManyToMany hoặc ForeignKey
    if not (request.user.id == section.teacher.id or
            not request.user.groups.filter(name='admins').exists()):
        return HttpResponseForbidden("Your dont have permission to access this feature")
    # Đảm bảo mỗi SV trong section có SubjectDetail
    details = []
    for s in students:
        detail, created = SubjectDetail.objects.get_or_create(
            student=s,
            subject=section.subject
        )
        details.append(detail)

    DetailFormSet = modelformset_factory(
        SubjectDetail,
        fields=('midterm', 'final', 'note'),
        extra=0
    )

    formset = DetailFormSet(queryset=SubjectDetail.objects.filter(id__in=[d.id for d in details]))

    if request.method == 'POST':
        formset = DetailFormSet(request.POST, queryset=SubjectDetail.objects.filter(id__in=[d.id for d in details]))
        if formset.is_valid():
            formset.save()
            return redirect('view_section', id=section.id)

    return render(request, 'classsections/enter_scores.html', {
        'section': section,
        'formset': formset
    })
