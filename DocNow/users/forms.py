from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, Doctor, Appiontment

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full'}))

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full'}),
            'email': forms.TextInput(attrs={'class': 'w-full'}),
        }

class EditUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo', 'phone', 'address1', 'address2', 'age', 'gender']

class AddDoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['photo','name', 'email', 'password', 'speciality', 'degree', 'experience', 'address1', 'address2', 'fees', 'about',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'email': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'password': forms.PasswordInput(attrs={'class': 'w-full','required':True}),
            'speciality': forms.Select(attrs={'class': 'w-full','required':True,'placeholder': 'Select an option'}),
            'degree': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'experience': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'address1': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'address2': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'fees': forms.TextInput(attrs={'class': 'w-full','required':True}),
            'about': forms.Textarea(attrs={'class': 'w-full','required':True}),
        }

class BookAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appiontment
        fields = ['appointment_date', 'appointment_time',]

        widgets = {
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'min': datetime.now().date().strftime('%Y-%m-%d'),
            }),
            'appointment_time': forms.Select(attrs={
                'class': 'form-select w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            now = datetime.now()
            today = now.date()

            if appointment_date == today:
                selected_datetime = datetime.combine(appointment_date, appointment_time)
                if selected_datetime <= now:
                    raise ValidationError('The selected time must be greater than the current time for today.')

        return cleaned_data


class DoctorLoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
         'class': 'form-control', 
         'placeholder': 'Email'
         }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if doctor.password != password:
                raise forms.ValidationError("Invalid email or password")
        except Doctor.DoesNotExist:
            raise forms.ValidationError("Invalid email or password")
        
        return cleaned_data

    