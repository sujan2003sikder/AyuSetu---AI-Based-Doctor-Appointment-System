from django.urls import path
from . import views

urlpatterns = [
    path('register/patient/', views.patient_register, name='patient_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('admin-dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path(
    'admin-doctors/',
    views.admin_doctor_verification,
    name='admin_doctor_verification'
    ),
    path(
    'admin-doctors/<int:doctor_id>/',
    views.admin_doctor_detail,
    name='admin_doctor_detail'
),
    path(
        'admin-doctors/<int:doctor_id>/approve/',
        views.admin_approve_doctor,
        name='admin_approve_doctor'
    ),

    path(
        'admin-doctors/<int:doctor_id>/reject/',
        views.admin_reject_doctor,
        name='admin_reject_doctor'
    ),
    path(
        'admin-patients/',
        views.admin_patient_management,
        name='admin_patient_management'
    ),
    path(
    'admin-patients/<int:patient_id>/',
    views.admin_patient_detail,
    name='admin_patient_detail'
),
    path(
        'admin-appointments/',
        views.admin_appointment_management,
        name='admin_appointment_management'
    ),
    path(
    'admin-appointments/<int:appointment_id>/',
    views.admin_appointment_detail,
    name='admin_appointment_detail'
),
    path(
        'admin-specializations/',
        views.admin_specialization_management,
        name='admin_specialization_management'
    ),
    
]