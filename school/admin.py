from django.contrib import admin

from .models import Notification, UserNotification

# Register your models here.
class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    extra = 1

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'created_at']
    inlines = [UserNotificationInline]

admin.site.register(Notification, NotificationAdmin)
