from django.contrib import admin
from .models import Parent,Student

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display =  ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    list_filter = ('father_name', 'mother_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display =  ('first_name', 'last_name',  'gender','date_of_birth','student_class','date_joined','mobile_number', 'email','major')
    search_fields = ('first_name', 'last_name','student__class')
    list_filter = ('gender','student_class','major')
    readonly_fields = ('student_image',)

    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name
    def date_joined(self, obj):
        return obj.user.date_joined
    def email(self, obj):
        return obj.user.email