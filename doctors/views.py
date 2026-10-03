from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import DoctorRegistrationForm, DoctorAvailabilityForm, DoctorProfileForm
from .models import DoctorProfile, DoctorAvailability

def approved_doctor_required(request):
    if request.user.role != 'doctor':
        return False
    try:
        doctor = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return False
    return doctor.verification_status == 'approved'
def doctor_register(request):

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = DoctorRegistrationForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Doctor registration submitted successfully. Your profile is awaiting admin verification.'
            )
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(
        request,
        'doctors/doctor_register.html',
        {'form': form}
    )
def doctor_list(request):
    doctors = DoctorProfile.objects.filter(
        verification_status='approved'
    ).select_related(
        'user',
        'specialization'
    )
    search = request.GET.get('search', '').strip()
    specialization_id = request.GET.get('specialization', '')
    if search:
        doctors = doctors.filter(
            user__first_name__icontains=search
        ) | doctors.filter(
            user__last_name__icontains=search
        ) | doctors.filter(
            user__username__icontains=search
        )
    if specialization_id:
        doctors = doctors.filter(
            specialization_id=specialization_id
        )
    from specializations.models import Specialization
    specializations = Specialization.objects.filter(
        is_active=True
    ).order_by('name')
    return render(
        request,
        'doctors/doctor_list.html',
        {
            'doctors': doctors.distinct(),
            'specializations': specializations,
            'search': search,
            'selected_specialization': specialization_id,
        }
    )
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(
        DoctorProfile.objects.select_related(
            'user',
            'specialization'
        ),
        id=doctor_id,
        verification_status='approved'
    )
    return render(
        request,
        'doctors/doctor_detail.html',
        {'doctor': doctor}
    )
@login_required
def manage_availability(request):
    if not approved_doctor_required(request):
     return redirect('home')
    doctor = get_object_or_404(
        DoctorProfile,
        user=request.user
    )

    if request.method == 'POST':

        form = DoctorAvailabilityForm(
        request.POST,
        doctor=doctor
    )

        if form.is_valid():

            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()

            messages.success(
                request,
                'Availability added successfully.'
            )

            return redirect('manage_availability')

    else:

        form = DoctorAvailabilityForm(
    doctor=doctor
)

    availabilities = doctor.availabilities.all().order_by(
        'day',
        'start_time'
    )

    return render(
        request,
        'doctors/manage_availability.html',
        {
            'form': form,
            'availabilities': availabilities
        }
    )
@login_required
def delete_availability(request, availability_id):

    if not approved_doctor_required(request):
        return redirect('home')

    if request.method != 'POST':
        return redirect('manage_availability')

    availability = get_object_or_404(
        DoctorAvailability,
        id=availability_id,
        doctor__user=request.user
    )

    availability.delete()

    messages.success(
        request,
        'Availability deleted successfully.'
    )

    return redirect('manage_availability')

@login_required
def doctor_profile(request):

    if request.user.role != 'doctor':
        return redirect('home')

    doctor = get_object_or_404(
        DoctorProfile.objects.select_related(
            'user',
            'specialization'
        ),
        user=request.user
    )

    if request.method == 'POST':

        form = DoctorProfileForm(
            request.POST,
            request.FILES,
            instance=doctor,
            user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Your doctor profile has been updated successfully.'
            )

            return redirect('doctor_profile')

    else:

        form = DoctorProfileForm(
            instance=doctor,
            user=request.user
        )

    return render(
        request,
        'doctors/doctor_profile.html',
        {
            'doctor': doctor,
            'form': form
        }
    )

@login_required
def doctor_dashboard(request):

    if not approved_doctor_required(request):
        return redirect('home')

    doctor = get_object_or_404(
        DoctorProfile.objects.select_related(
            'user',
            'specialization'
        ),
        user=request.user
    )

    appointments = doctor.appointments.select_related(
        'patient'
    )

    today = date.today()

    today_appointments = appointments.filter(
        appointment_date=today
    ).order_by(
        'appointment_time'
    )

    pending_count = appointments.filter(
        status='pending'
    ).count()

    confirmed_count = appointments.filter(
        status='confirmed'
    ).count()

    completed_count = appointments.filter(
        status='completed'
    ).count()

    return render(
        request,
        'doctors/doctor_dashboard.html',
        {
            'doctor': doctor,
            'today_appointments': today_appointments,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'completed_count': completed_count,
        }
    )