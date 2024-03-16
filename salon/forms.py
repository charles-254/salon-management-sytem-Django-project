from django import forms
from .models import Appointment, CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username', 'Username already exists.')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists.')
        if CustomUser.objects.filter(phone=phone).exists():
            self.add_error('phone', 'Phone number already exists.')

        return cleaned_data

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SalonAppointmentForm(forms.Form):
    stylist_name = forms.CharField()
    stylist_specialty = forms.CharField()
    price = forms.IntegerField()
    customuser_username = forms.CharField(widget=forms.HiddenInput())
    appointment_date_time = forms.DateTimeField(
        label='Date and Time',
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'})
    )
class EditDetailsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs['initial'] = {
                'username': instance.username,
                'email': instance.email,
                'phone': instance.phone,
            }
        super().__init__(*args, **kwargs)

