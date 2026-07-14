from django import forms
from django.contrib.auth.models import User
from .models import Task, Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']