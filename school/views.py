from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render

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

