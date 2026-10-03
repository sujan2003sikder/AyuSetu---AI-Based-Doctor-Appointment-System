from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import PatientRegistrationForm, PatientProfileForm
from .models import PatientProfile, User
from doctors.models import DoctorProfile
from appointments.models import Appointment
from specializations.models import Specialization

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    total_doctors = DoctorProfile.objects.count()
    pending_doctors = DoctorProfile.objects.filter(
        verification_status='pending'
    ).count()
    approved_doctors = DoctorProfile.objects.filter(
        verification_status='approved'
    ).count()
    rejected_doctors = DoctorProfile.objects.filter(
    verification_status='rejected'
    ).count()
    total_patients = request.user.__class__.objects.filter(
        role='patient'
    ).count()
    total_appointments = Appointment.objects.count()
    total_specializations = Specialization.objects.filter(
        is_active=True
    ).count()
    recent_appointments = Appointment.objects.select_related(
    'patient',
    'doctor__user',
    'doctor__specialization'
).order_by(
    '-created_at'
)[:5]
    pending_doctor_list = DoctorProfile.objects.select_related(
    'user',
    'specialization'
).filter(
    verification_status='pending'
).order_by(
    '-created_at'
)[:5]
    return render(
        request,
        'accounts/admin_dashboard.html',
        {
        'total_doctors': total_doctors,
        'pending_doctors': pending_doctors,
        'approved_doctors': approved_doctors,
        'rejected_doctors': rejected_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_specializations': total_specializations,
        'recent_appointments': recent_appointments,
        'pending_doctor_list': pending_doctor_list,
        }
    )
def patient_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Patient account created successfully. Please login.'
            )
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(
        request,
        'accounts/patient_register.html',
        {'form': form}
    )

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('home')
        messages.error(
            request,
            'Invalid username or password.'
        )
    return render(
        request,
        'accounts/login.html',
        {
            'next': next_url
        }
    )
def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def patient_profile(request):
    if request.user.role != 'patient':
        return redirect('home')
    profile = get_object_or_404(
        PatientProfile,
        user=request.user
    )
    if request.method == 'POST':
        form = PatientProfileForm(
            request.POST,
            instance=profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('patient_profile')
    else:
        form = PatientProfileForm(
            instance=profile,
            user=request.user
        )
    return render(
        request,
        'accounts/patient_profile.html',
        {
            'profile': profile,
            'form': form
        }
    )
@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('home')
    appointments = request.user.appointments.select_related(
        'doctor__user',
        'doctor__specialization'
    )
    today = date.today()
    total_count = appointments.count()
    pending_count = appointments.filter(
        status='pending'
    ).count()
    confirmed_count = appointments.filter(
        status='confirmed'
    ).count()
    completed_count = appointments.filter(
        status='completed'
    ).count()
    upcoming_appointments = appointments.filter(
        appointment_date__gte=today,
        status__in=['pending', 'confirmed']
    ).order_by(
        'appointment_date',
        'appointment_time'
    )[:5]
    return render(
        request,
        'accounts/patient_dashboard.html',
        {
            'total_count': total_count,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'completed_count': completed_count,
            'upcoming_appointments': upcoming_appointments,
        }
    )
@login_required
def admin_doctor_verification(request):
    if not request.user.is_staff:
        return redirect('home')
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()
    doctors = DoctorProfile.objects.select_related(
        'user',
        'specialization'
    ).order_by(
        'verification_status',
        '-created_at'
    )
    if status_filter in ['pending', 'approved', 'rejected']:
        doctors = doctors.filter(
            verification_status=status_filter
        )
    if search_query:
        from django.db.models import Q
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(specialization__name__icontains=search_query)
        )
    return render(
        request,
        'accounts/admin_doctor_verification.html',
        {
            'doctors': doctors,
            'status_filter': status_filter,
            'search_query': search_query,
        }
    )
@login_required
def admin_doctor_detail(request, doctor_id):
    if not request.user.is_staff:
        return redirect('home')
    doctor = get_object_or_404(
        DoctorProfile.objects.select_related(
            'user',
            'specialization'
        ),
        id=doctor_id
    )
    availabilities = doctor.availabilities.filter(
        is_active=True
    ).order_by(
        'day',
        'start_time'
    )
    return render(
        request,
        'accounts/admin_doctor_detail.html',
        {
            'doctor': doctor,
            'availabilities': availabilities,
        }
    )
@login_required
def admin_approve_doctor(request, doctor_id):

    if not request.user.is_staff:
        return redirect('home')

    if request.method != 'POST':
        return redirect('admin_doctor_verification')

    doctor = get_object_or_404(
        DoctorProfile,
        id=doctor_id
    )

    doctor.verification_status = 'approved'
    doctor.save()

    messages.success(
        request,
        f'{doctor} has been approved successfully.'
    )

    return redirect('admin_doctor_verification')


@login_required
def admin_reject_doctor(request, doctor_id):

    if not request.user.is_staff:
        return redirect('home')

    if request.method != 'POST':
        return redirect('admin_doctor_verification')

    doctor = get_object_or_404(
        DoctorProfile,
        id=doctor_id
    )

    doctor.verification_status = 'rejected'
    doctor.save()

    messages.success(
        request,
        f'{doctor} has been rejected.'
    )

    return redirect('admin_doctor_verification')

@login_required
def admin_patient_management(request):

    if not request.user.is_staff:
        return redirect('home')

    search_query = request.GET.get('search', '').strip()

    patients = User.objects.filter(
        role='patient'
    ).select_related(
        'patient_profile'
    ).order_by(
        '-date_joined'
    )

    if search_query:
        from django.db.models import Q

        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    return render(
        request,
        'accounts/admin_patient_management.html',
        {
            'patients': patients,
            'search_query': search_query,
        }
    )
@login_required
def admin_appointment_management(request):

    if not request.user.is_staff:
        return redirect('home')

    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()

    appointments = Appointment.objects.select_related(
        'patient',
        'doctor__user',
        'doctor__specialization'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    if status_filter in [
        'pending',
        'confirmed',
        'completed',
        'rejected',
        'cancelled'
    ]:
        appointments = appointments.filter(
            status=status_filter
        )

    if search_query:
        from django.db.models import Q

        appointments = appointments.filter(
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__username__icontains=search_query) |
            Q(patient__email__icontains=search_query) |
            Q(doctor__user__first_name__icontains=search_query) |
            Q(doctor__user__last_name__icontains=search_query) |
            Q(doctor__user__username__icontains=search_query) |
            Q(doctor__specialization__name__icontains=search_query)
        )

    return render(
        request,
        'accounts/admin_appointment_management.html',
        {
            'appointments': appointments,
            'status_filter': status_filter,
            'search_query': search_query,
        }
    )
@login_required
def admin_specialization_management(request):

    if not request.user.is_staff:
        return redirect('home')

    search_query = request.GET.get('search', '').strip()

    specializations = Specialization.objects.order_by('name')

    if search_query:
        specializations = specializations.filter(
            name__icontains=search_query
        )

    return render(
        request,
        'accounts/admin_specialization_management.html',
        {
            'specializations': specializations,
            'search_query': search_query,
        }
    )
@login_required
def admin_patient_detail(request, patient_id):

    if not request.user.is_staff:
        return redirect('home')

    patient = get_object_or_404(
        User.objects.select_related('patient_profile'),
        id=patient_id,
        role='patient'
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        'doctor__user',
        'doctor__specialization'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'accounts/admin_patient_detail.html',
        {
            'patient': patient,
            'appointments': appointments,
        }
    )
@login_required
def admin_appointment_detail(request, appointment_id):

    if not request.user.is_staff:
        return redirect('home')

    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'patient',
            'doctor__user',
            'doctor__specialization'
        ),
        id=appointment_id
    )

    return render(
        request,
        'accounts/admin_appointment_detail.html',
        {
            'appointment': appointment,
        }
    )
