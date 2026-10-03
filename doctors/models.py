from django.conf import settings
from django.db import models

class DoctorProfile(models.Model):
    VERIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    registration_number = models.CharField(
        max_length=100,
        unique=True
    )
    qualification = models.CharField(max_length=255)
    specialization = models.ForeignKey(
    'specializations.Specialization',
    on_delete=models.PROTECT,
    related_name='doctors'
)
    experience = models.PositiveIntegerField(
        help_text='Experience in years'
    )
    clinic_name = models.CharField(
        max_length=255,
        blank=True
    )
    clinic_address = models.TextField(
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    profile_image = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class DoctorAvailability(models.Model):

    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    day = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return (
            f"{self.doctor} - "
            f"{self.get_day_display()} "
            f"{self.start_time} - "
            f"{self.end_time}"
        )
