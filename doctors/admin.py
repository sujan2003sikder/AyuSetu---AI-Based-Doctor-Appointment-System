from django.contrib import admin
from .models import DoctorProfile, DoctorAvailability
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):

    list_display = (
        'doctor_name',
        'registration_number',
        'specialization',
        'qualification',
        'experience',
        'verification_status',
        'created_at',
    )

    list_filter = (
        'verification_status',
        'specialization',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'registration_number',
        'qualification',
    )

    ordering = (
        'verification_status',
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (
            'Doctor Account',
            {
                'fields': (
                    'user',
                )
            }
        ),

        (
            'Professional Information',
            {
                'fields': (
                    'registration_number',
                    'qualification',
                    'specialization',
                    'experience',
                )
            }
        ),

        (
            'Clinic Information',
            {
                'fields': (
                    'clinic_name',
                    'clinic_address',
                )
            }
        ),

        (
            'Profile',
            {
                'fields': (
                    'bio',
                    'profile_image',
                )
            }
        ),

        (
            'Verification',
            {
                'fields': (
                    'verification_status',
                )
            }
        ),

        (
            'System Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    def doctor_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    doctor_name.short_description = 'Doctor'


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):

    list_display = (
        'doctor',
        'day',
        'start_time',
        'end_time',
        'is_active',
    )

    list_filter = (
        'day',
        'is_active',
    )

    search_fields = (
        'doctor__user__username',
        'doctor__user__first_name',
        'doctor__user__last_name',
    )