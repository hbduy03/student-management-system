from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.teacher_list, name='teacher_list'),

]