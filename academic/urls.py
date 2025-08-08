from django.urls import path

from . import views

urlpatterns = [
    # ---------- URL DEPARTMENT --------
    path('department/', views.department_list, name='department_list'),
    path('department/add/',views.add_department, name='add_department'),
    path('department/edit/<str:id>', views.edit_department, name='edit_department'),
    path('department/delete/<str:id>', views.delete_department, name='delete_department'),

    # ---------- URL MAJOR --------
    path('major/', views.major_list, name='major_list'),
    path('major/add/', views.add_major, name='add_major'),
    path('major/edit/<str:id>', views.edit_major, name='edit_major'),
    path('major/delete/<str:id>', views.delete_major, name='delete_major'),
]