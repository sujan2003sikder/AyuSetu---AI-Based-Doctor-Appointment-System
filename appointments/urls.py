from django.urls import path

from . import views


urlpatterns = [
    path(
        'book/<int:doctor_id>/',
        views.book_appointment,
        name='book_appointment'
    ),

    path(
        'doctor/',
        views.doctor_appointments,
        name='doctor_appointments'
    ),

    path(
        'doctor/<int:appointment_id>/confirm/',
        views.confirm_appointment,
        name='confirm_appointment'
    ),

    path(
        'doctor/<int:appointment_id>/reject/',
        views.reject_appointment,
        name='reject_appointment'
    ),

    path(
        'doctor/<int:appointment_id>/complete/',
        views.complete_appointment,
        name='complete_appointment'
    ),

    path(
        'my/',
        views.patient_appointments,
        name='patient_appointments'
    ),

    path(
        'my/<int:appointment_id>/',
        views.appointment_detail,
        name='appointment_detail'
    ),

    path(
        'my/<int:appointment_id>/cancel/',
        views.cancel_appointment,
        name='cancel_appointment'
    ),
]