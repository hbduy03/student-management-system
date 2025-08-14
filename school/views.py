from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import redirect

from student.models import Student
from teacher.models import Teacher
from .models import UserNotification, Notification


def index(request):
    return render(request, 'authentication/login.html')

def dashboard(request):
    if request.user.groups.filter(name='admins').exists():
        return render(request, 'Home/index.html')
    elif request.user.groups.filter(name='teachers').exists():
        return render(request, 'teachers/teacher-dashboard.html')
    else:
        return render(request, 'students/student-dashboard.html')

def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = UserNotification.objects.filter(user = request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden

def clear_all_notifications(request):
    if request.method == 'POST':
        notification = UserNotification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden

def create_notification(user, message):
    noti = Notification.objects.create(message=message)
    UserNotification.objects.create(user=user, notification = noti)


def my_profile(request):
    user = request.user

    if user.groups.filter(name='teachers').exists():
        teacher = Teacher.objects.get(user=user)
        return redirect('view_teacher', slug=teacher.slug)

    elif user.groups.filter(name='students').exists():
        student = Student.objects.get(user=user)
        return redirect('view_student', slug=student.slug)

    return redirect('dashboard')
