from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import uuid
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique= True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    pass

class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    email =models.EmailField()
    token = models.CharField(max_length=32, default= get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add= True)
    TOKEN_VALIDITY_PERIOD = timedelta(hours=0.1)
    def is_valid(self):
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f'http://localhost:8000/authentication/reset-password/{self.token}/'
        send_mail(
            f'Yêu cầu thay đổi mật khẩu {self.user.username} trên PRESKOOL',
            f'''Nhấn vào link bên dưới để thay đổi mật khẩu.
Link sẽ hết hiệu lực trong vòng 10: {reset_link}''',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently = False,
        )