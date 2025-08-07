from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.teacher_list, name='teacher_list'),
    path('add/',views.add_teacher, name='add_teacher'),
    path('teachers/<str:slug>', views.view_teacher, name='view_teacher'),
    path('edit/<str:slug>', views.edit_teacher, name='edit_teacher'),
    path('delete/<str:slug>', views.delete_teacher, name='delete_teacher'),

]