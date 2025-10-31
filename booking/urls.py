from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # Other URL patterns...
    path('register/', views.registration_view, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-classes/', views.ClassListView.as_view(), name='admin_class_list'),
    path('admin-classes/add/', views.ClassCreateView.as_view(), name='admin_class_add'),
    path('admin-classes/<int:pk>/edit/', views.ClassUpdateView.as_view(), name='admin_class_edit'),
    path('admin-classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='admin_class_delete'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-student-to-teacher/', views.add_student_to_teacher, name='add_student_to_teacher'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-class/', views.add_class, name='add_class'),
    path('modify-balance/', views.modify_balance, name='modify_balance'),
    path('cancel_class/', views.cancel_class, name='cancel_class'),    
    path('add_class_for_teacher/', views.add_class_for_teacher, name='add_class_for_teacher'),

]
