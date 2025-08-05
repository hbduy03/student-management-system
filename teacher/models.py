from django.db import models
from django.db.models import ForeignKey, OneToOneField
from django.utils.text import slugify

from academic.models import Classroom, Department
from home_auth.models import CustomUser


class Teacher(models.Model):
    user = OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    teacher_image = models.ImageField(upload_to='teacher/', blank=True)
    slug = models.SlugField(max_length=255, unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.first_name}-{self.user.last_name}-{self.teacher_id}')
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.teacher_id})'