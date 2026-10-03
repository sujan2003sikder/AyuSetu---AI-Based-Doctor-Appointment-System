from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from .models import DoctorProfile, DoctorAvailability


class DoctorRegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150
    )

    last_name = forms.CharField(
        max_length=150
    )

    email = forms.EmailField()

    phone = forms.CharField(
        max_length=15
    )

    registration_number = forms.CharField(
        max_length=100
    )

    qualification = forms.CharField(
        max_length=255
    )

    specialization = forms.ModelChoiceField(
        queryset=None
    )

    experience = forms.IntegerField(
        min_value=0
    )

    

    clinic_name = forms.CharField(
        max_length=255,
        required=False
    )

    clinic_address = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    bio = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    profile_image = forms.ImageField(
        required=False
    )

    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        from specializations.models import Specialization

        self.fields['specialization'].queryset = (
            Specialization.objects.filter(
                is_active=True
            )
        )

    def clean_registration_number(self):

        registration_number = (
            self.cleaned_data['registration_number'].strip()
        )

        if DoctorProfile.objects.filter(
            registration_number=registration_number
        ).exists():

            raise forms.ValidationError(
                'This registration number is already registered.'
            )

        return registration_number

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = 'doctor'

        if commit:

            user.save()

            DoctorProfile.objects.create(
                user=user,
                registration_number=self.cleaned_data[
                    'registration_number'
                ],
                qualification=self.cleaned_data[
                    'qualification'
                ],
                specialization=self.cleaned_data[
                    'specialization'
                ],
                experience=self.cleaned_data[
                    'experience'
                ],
                
                clinic_name=self.cleaned_data[
                    'clinic_name'
                ],
                clinic_address=self.cleaned_data[
                    'clinic_address'
                ],
                bio=self.cleaned_data[
                    'bio'
                ],
                profile_image=self.cleaned_data[
                    'profile_image'
                ]
            )

        return user


class DoctorAvailabilityForm(forms.ModelForm):

    class Meta:

        model = DoctorAvailability

        fields = (
            'day',
            'start_time',
            'end_time',
        )

        widgets = {

            'start_time': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time'
                }
            ),

            'end_time': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        self.doctor = kwargs.pop('doctor', None)

        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        day = cleaned_data.get('day')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:

            if start_time >= end_time:

                raise forms.ValidationError(
                    'End time must be later than start time.'
                )

        if self.doctor and day and start_time and end_time:

            overlapping = DoctorAvailability.objects.filter(
                doctor=self.doctor,
                day=day,
                is_active=True,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if self.instance.pk:

                overlapping = overlapping.exclude(
                    pk=self.instance.pk
                )

            if overlapping.exists():

                raise forms.ValidationError(
                    'This availability overlaps with an existing schedule.'
                )

        return cleaned_data


class DoctorProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    email = forms.EmailField()

    phone = forms.CharField(
        max_length=15,
        required=False
    )

    class Meta:

        model = DoctorProfile

        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'qualification',
            'specialization',
            'experience',
            'clinic_name',
            'clinic_address',
            'bio',
            'profile_image',
        )

        widgets = {

            'clinic_address': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter clinic address'
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': (
                        'Write about your professional experience'
                    )
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields['first_name'].initial = (
                user.first_name
            )

            self.fields['last_name'].initial = (
                user.last_name
            )

            self.fields['email'].initial = (
                user.email
            )

            self.fields['phone'].initial = (
                user.phone
            )

        self.user = user

        self.fields['specialization'].queryset = (
            self.fields['specialization'].queryset.filter(
                is_active=True
            )
        )

    def save(self, commit=True):

        doctor = super().save(commit=False)

        if self.user:

            self.user.first_name = (
                self.cleaned_data['first_name']
            )

            self.user.last_name = (
                self.cleaned_data['last_name']
            )

            self.user.email = (
                self.cleaned_data['email']
            )

            self.user.phone = (
                self.cleaned_data['phone']
            )

            if commit:
                self.user.save()

        if commit:
            doctor.save()

        return doctor