from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Specialization


def specialization_list(request):

    specializations = Specialization.objects.filter(
        is_active=True
    ).annotate(
        approved_doctor_count=Count(
            'doctors',
            filter=Q(
                doctors__verification_status='approved'
            )
        )
    )

    return render(
        request,
        'specializations/specialization_list.html',
        {
            'specializations': specializations
        }
    )


def specialization_doctors(request, specialization_id):

    specialization = get_object_or_404(
        Specialization,
        id=specialization_id,
        is_active=True
    )

    doctors = specialization.doctors.filter(
        verification_status='approved'
    ).select_related('user', 'specialization')

    return render(
        request,
        'specializations/specialization_doctors.html',
        {
            'specialization': specialization,
            'doctors': doctors
        }
    )