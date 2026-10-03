from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'appointment_date',
    )

    search_fields = (
        'patient__username',
        'patient__first_name',
        'patient__last_name',
        'doctor__user__username',
        'doctor__user__first_name',
        'doctor__user__last_name',
    )

    ordering = (
        '-appointment_date',
        '-appointment_time',
    )