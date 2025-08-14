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

    # ---------- URL SUBJECT --------
    path('subject/', views.subject_list, name='subject_list'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('subject/edit/<str:id>', views.edit_subject, name='edit_subject'),
    path('subject/delete/<str:id>', views.delete_subject, name='delete_subject'),

    # ---------- URL CLASSROOM --------
    path('classroom/', views.classroom_list, name='classroom_list'),
    path('classroom/add/', views.add_classroom, name='add_classroom'),
    path('classroom/edit/<str:id>', views.edit_classroom, name='edit_classroom'),
    path('classroom/delete/<str:id>', views.delete_classroom, name='delete_classroom'),

    # ---------- URL CLASSSECTION --------
    path('classsection/', views.section_list, name='section_list'),
    path('classsection/add/', views.add_section, name='add_section'),
    path('classsection/edit/<str:id>', views.edit_section, name='edit_section'),
    path('classsection/delete/<str:id>', views.delete_section, name='delete_section'),
    path('classsection/<str:id>', views.view_section, name='view_section'),
    path('classsection/<str:id>/add/', views.add_student_section, name='add_student_section'),
    path('classsection/<str:section_id>/enter-scores/', views.enter_scores, name='enter_scores'),
    path('classsection/<str:id>/predict/', views.view_predict, name='view_predict'),

]