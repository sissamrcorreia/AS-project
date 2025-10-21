from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile
import datetime

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

class CustomFileInput(forms.ClearableFileInput):
    template_name = 'widgets/custom_file_input.html'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'birthdate', 'avatar']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'add a phone number'
            }),
            'birthdate': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'max': datetime.date.today().isoformat(),
            }),
            'avatar': CustomFileInput(),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get("birthdate")
        if not birthdate:
            return birthdate

        today = datetime.date.today()

        age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
        )
        if age < 16:
            raise forms.ValidationError("You must be 16 years old to use GoodBite")
        return birthdate
