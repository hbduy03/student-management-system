import uuid

from django.conf import settings
from django.db import models

# Create your models here.

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable= False )
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="user_notifications")
    is_read = models.BooleanField(default=False)

