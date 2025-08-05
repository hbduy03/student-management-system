from django.db import models
from django.db.models import OneToOneField
from django.utils.text import slugify

from academic.models import Classroom, Major
from home_auth.models import CustomUser


# Create your models here.
class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=100)
    father_email = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=100)
    mother_email = models.CharField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self) -> str:
        return f'{self.father_name} &  {self.mother_name}'

class Student(models.Model):
    user = OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    student_class = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    student_image = models.ImageField(upload_to='student/profile/', blank=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.first_name}-{self.user.last_name}-{self.user.username}')
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'