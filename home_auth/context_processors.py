from school.models import UserNotification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notification': UserNotification.objects.select_related('notification').filter(user=request.user, is_read=False),
            'unread_notification_count': UserNotification.objects.select_related('notification').filter(user=request.user, is_read=False).count()
        }
    return {}