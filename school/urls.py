from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('my-profile/', views.my_profile, name='my_profile'),
]