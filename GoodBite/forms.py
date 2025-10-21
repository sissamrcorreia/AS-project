from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'birthdate']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Add phone number…'
            }),
            'birthdate': forms.DateInput(attrs={
                'type': 'date',  # datepicker nativo
                'placeholder': 'YYYY-MM-DD'
            }),
        }

    # block for no future dates and if birthdate is less tah  16 years ago, message error
    # also add the picture thing