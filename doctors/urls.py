from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('register/', views.doctor_register, name='doctor_register'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('availability/', views.manage_availability, name='manage_availability'),
    path(
        'availability/delete/<int:availability_id>/',
        views.delete_availability,
        name='delete_availability'
    ),
    path('profile/', views.doctor_profile, name='doctor_profile'),
]