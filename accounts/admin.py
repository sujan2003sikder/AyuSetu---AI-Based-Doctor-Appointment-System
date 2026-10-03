from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import User, PatientProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('AyuSetu Information', {
            'fields': ('phone', 'role'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('AyuSetu Information', {
            'fields': ('email', 'phone', 'role'),
        }),
    )

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date_of_birth',
        'gender',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )