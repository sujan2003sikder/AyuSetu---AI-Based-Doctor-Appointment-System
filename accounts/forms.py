from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientProfile


class PatientRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

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

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = 'patient'

        if commit:
            user.save()

            PatientProfile.objects.create(
                user=user
            )

        return user
class PatientProfileForm(forms.ModelForm):

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
        model = PatientProfile
        fields = (
            'date_of_birth',
            'gender',
            'address',
        )

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'gender': forms.Select(
                choices=[
                    ('', 'Select Gender'),
                    ('Male', 'Male'),
                    ('Female', 'Female'),
                    ('Other', 'Other'),
                ]
            ),
            'address': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter your address'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone

        self.user = user

    def save(self, commit=True):

        profile = super().save(commit=False)

        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.phone = self.cleaned_data['phone']

            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile