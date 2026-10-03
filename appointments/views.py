from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from doctors.models import DoctorProfile, DoctorAvailability
from doctors.views import approved_doctor_required

from .forms import AppointmentBookingForm
from .models import Appointment


def generate_time_slots(start_time, end_time):

    slots = []

    current_time = datetime.combine(
        date.today(),
        start_time
    )

    end_datetime = datetime.combine(
        date.today(),
        end_time
    )

    while current_time < end_datetime:

        slots.append(current_time.time())

        current_time += timedelta(minutes=30)

    return slots


@login_required
def book_appointment(request, doctor_id):

    if request.user.role != 'patient':
        return redirect('home')

    doctor = get_object_or_404(
        DoctorProfile.objects.select_related(
            'user',
            'specialization'
        ),
        id=doctor_id,
        verification_status='approved'
    )

    selected_date = (
        request.POST.get('appointment_date')
        or request.GET.get('appointment_date')
    )

    available_slots = []

    if selected_date:

        try:

            selected_date_obj = datetime.strptime(
                selected_date,
                '%Y-%m-%d'
            ).date()

            if selected_date_obj >= date.today():

                weekday = selected_date_obj.strftime('%A').lower()

                availabilities = DoctorAvailability.objects.filter(
                    doctor=doctor,
                    day=weekday,
                    is_active=True
                ).order_by('start_time')

                booked_times = set(
                    Appointment.objects.filter(
                        doctor=doctor,
                        appointment_date=selected_date_obj,
                        status__in=[
                            'pending',
                            'confirmed'
                        ]
                    ).values_list(
                        'appointment_time',
                        flat=True
                    )
                )

                for availability in availabilities:

                    slots = generate_time_slots(
                        availability.start_time,
                        availability.end_time
                    )

                    for slot in slots:

                        if slot not in booked_times:
                            available_slots.append(slot)

        except ValueError:

            selected_date = None

    if request.method == 'POST':

        form = AppointmentBookingForm(request.POST)

        if form.is_valid():

            appointment_date = form.cleaned_data[
                'appointment_date'
            ]

            appointment_time = form.cleaned_data[
                'appointment_time'
            ]

            weekday = appointment_date.strftime('%A').lower()

            available = DoctorAvailability.objects.filter(
                doctor=doctor,
                day=weekday,
                start_time__lte=appointment_time,
                end_time__gt=appointment_time,
                is_active=True
            ).exists()

            if appointment_date < date.today():

                form.add_error(
                    'appointment_date',
                    'You cannot book an appointment for a past date.'
                )

            elif not available:

                form.add_error(
                    'appointment_time',
                    'The doctor is not available at this time.'
                )

            else:

                valid_slot = False

                availabilities = DoctorAvailability.objects.filter(
                    doctor=doctor,
                    day=weekday,
                    is_active=True
                )

                for availability in availabilities:

                    slots = generate_time_slots(
                        availability.start_time,
                        availability.end_time
                    )

                    if appointment_time in slots:

                        valid_slot = True
                        break

                if not valid_slot:

                    form.add_error(
                        'appointment_time',
                        'Please select a valid 30-minute appointment slot.'
                    )

                elif Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=[
                        'pending',
                        'confirmed'
                    ]
                ).exists():

                    form.add_error(
                        'appointment_time',
                        'This time slot is already booked.'
                    )

                else:

                    appointment = form.save(commit=False)

                    appointment.patient = request.user
                    appointment.doctor = doctor
                    appointment.status = 'pending'

                    appointment.save()

                    messages.success(
                        request,
                        'Appointment booked successfully. '
                        'Waiting for doctor confirmation.'
                    )

                    return redirect(
                        'doctor_detail',
                        doctor_id=doctor.id
                    )

    else:

        form = AppointmentBookingForm()

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'form': form,
            'doctor': doctor,
            'available_slots': available_slots,
            'selected_date': selected_date,
            'today': date.today(),
        }
    )


@login_required
def doctor_appointments(request):

    if not approved_doctor_required(request):
        return redirect('home')

    appointments = Appointment.objects.filter(
        doctor__user=request.user
    ).select_related(
        'patient',
        'doctor__user'
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    return render(
        request,
        'appointments/doctor_appointments.html',
        {
            'appointments': appointments
        }
    )


@login_required
def confirm_appointment(request, appointment_id):

    if not approved_doctor_required(request):
        return redirect('home')

    if request.method != 'POST':
        return redirect('doctor_appointments')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor__user=request.user
    )

    if appointment.status == 'pending':

        appointment.status = 'confirmed'

        appointment.save()

        messages.success(
            request,
            'Appointment confirmed successfully.'
        )

    return redirect('doctor_appointments')

@login_required
def reject_appointment(request, appointment_id):

    if not approved_doctor_required(request):
        return redirect('home')

    if request.method != 'POST':
        return redirect('doctor_appointments')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor__user=request.user
    )

    if appointment.status == 'pending':

        appointment.status = 'rejected'

        appointment.save()

        messages.success(
            request,
            'Appointment rejected.'
        )

    return redirect('doctor_appointments')

@login_required
def complete_appointment(request, appointment_id):

    if not approved_doctor_required(request):
        return redirect('home')

    if request.method != 'POST':
        return redirect('doctor_appointments')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor__user=request.user
    )

    if appointment.status == 'confirmed':

        appointment.status = 'completed'

        appointment.save()

        messages.success(
            request,
            'Appointment marked as completed.'
        )

    return redirect('doctor_appointments')


@login_required
def patient_appointments(request):

    if request.user.role != 'patient':
        return redirect('home')

    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related(
        'doctor__user',
        'doctor__specialization'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'appointments/patient_appointments.html',
        {
            'appointments': appointments
        }
    )

@login_required
def appointment_detail(request, appointment_id):

    if request.user.role != 'patient':
        return redirect('home')

    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'doctor__user',
            'doctor__specialization'
        ),
        id=appointment_id,
        patient=request.user
    )

    return render(
        request,
        'appointments/appointment_detail.html',
        {
            'appointment': appointment
        }
    )


@login_required
def cancel_appointment(request, appointment_id):

    if request.user.role != 'patient':
        return redirect('home')

    if request.method != 'POST':
        return redirect('patient_appointments')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    if appointment.status in ['pending', 'confirmed']:

        appointment.status = 'cancelled'

        appointment.save()

        messages.success(
            request,
            'Appointment cancelled successfully.'
        )

    else:

        messages.error(
            request,
            'This appointment cannot be cancelled.'
        )

    return redirect('patient_appointments')