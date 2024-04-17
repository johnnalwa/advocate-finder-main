from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.db import transaction
from .models import *
from django import forms
from django.contrib.auth import get_user_model
from .models import LawyerProfile



User = get_user_model()

class MemberSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control radius-30 ps-5"}), label=("Email"))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label=("Username"))
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={"class": "form-control radius-30 ps-5"}))
    password2 = forms.CharField(label=("Confirm Password"), widget=forms.PasswordInput(attrs={"class": "form-control radius-30 ps-5"}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label="Last Name")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        if commit:
            user.save()
        client = Client.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'))
        return user
    


class AdvocatesSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control radius-30 ps-5"}), label=("Email"))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label=("Username"))
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={"class": "form-control radius-30 ps-5"}))
    password2 = forms.CharField(label=("Confirm Password"), widget=forms.PasswordInput(attrs={"class": "form-control radius-30 ps-5"}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label="Last Name")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_advocate = True
        if commit:
            user.save()
        personell = AdvocateAdmin.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'))
        return user
    


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control radius-30 ps-5"}), label=("Username"))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={"class": "form-control radius-30 ps-5"}))
   


class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = LawyerProfile
        exclude = ['user', 'created_at']  # Excluding fields not directly handled by the form


class AdvocateForm(forms.ModelForm):
    class Meta:
        model = Advocate
        fields = ['specialization', 'experience_years', 'hourly_rate', 'is_available']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = LawyerProfile
        fields = "__all__"


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'client', 'case_type'] 