from django.db import models

class Department(models.Model):
    department_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    hod = models.OneToOneField('teacher.Teacher', on_delete=models.SET_NULL, blank=True, null=True, related_name='header_department')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Major (models.Model):
    major_id = models.CharField(max_length=10,
                                unique=True)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create your models here.
class Subject(models.Model):
    subject_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    attribute = models.IntegerField(null=True, blank=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SubjectDetail(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.SET_NULL, blank=True, null = True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null = True)
    midterm =   models.FloatField(null=True, blank=True)
    final  = models.FloatField(null=True, blank=True)
    overall =models.FloatField(null=True, blank=True)
    GPA =   models.FloatField(null=True, blank=True)
    rank =  models.CharField(max_length=1, choices=[
                                                    ('A', 'A'),
                                                    ('B', 'B'),
                                                    ('C', 'C'),
                                                    ('D', 'D'),
                                                    ('F', 'F')
                                                                ],null=True,blank=True)
    passed = models.BooleanField(null=True, blank=True)
    note    = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} ({self.student.student_id}) {self.overall} ({self.passed})'

class Classroom(models.Model):
    name = models.CharField(max_length=50)
    home_teacher = models.ForeignKey('teacher.Teacher', null=True,blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class ClassSection(models.Model):
    classroom = models.ForeignKey(Classroom, null=True, blank=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey('teacher.Teacher', null=True, blank=True, on_delete=models.SET_NULL)
    students = models.ManyToManyField('student.Student', blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


