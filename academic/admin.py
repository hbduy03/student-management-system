from django.contrib import admin

from academic.models import Department, Major, Subject, SubjectDetail, Classroom, ClassSection
from student.models import Student

class StudentInline(admin.TabularInline):
    model = ClassSection.students.through  # hiển thị chỉ những học sinh đã liên kết với lớp
    extra = 0

class ClassSectionAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    exclude = ('students',)  # bỏ widget SelectMultiple mặc định

class SubjectDetailInline(admin.TabularInline):
    model = SubjectDetail
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [SubjectDetailInline]

admin.site.register(ClassSection, ClassSectionAdmin)
admin.site.register(Classroom)
# Register your models here.
admin.site.register(Department)
admin.site.register(Major)
admin.site.register(Subject, SubjectAdmin)