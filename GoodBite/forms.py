from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Product, Profile
import datetime
from allauth.account.internal.flows.login import record_authentication

class CustomSignupForm(SignupForm):
    username  = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "YYYY-MM-DD",
                "max": datetime.date.today().isoformat(),
            }
        ),
        help_text="You must be at least 16 years old.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].max_length = 30
        self.fields["username"].widget.attrs["maxlength"] = 30
        self.fields["username"].help_text = "Max 30 characters."
        self.fields["first_name"].help_text = "Max 30 characters."
        self.fields["last_name"].help_text = "Max 30 characters."

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get("birthdate")
        if not birthdate:
            raise forms.ValidationError("Birthdate is required.")

        today = datetime.date.today()
        age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
        )
        if age < 16:
            raise forms.ValidationError("You must be at least 16 years old to use GoodBite")

        return birthdate

    def save(self, request):
        user = super().save(request)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "birthdate": self.cleaned_data.get("birthdate"),
            }
        )
        username_or_email = (
                self.cleaned_data.get("username")
                or self.cleaned_data.get("email")
        )

        record_authentication(
            request,
            user,
            method="password",
            email=username_or_email
        )
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        try:
            local_part, domain = email.rsplit("@", 1)
        except ValueError:
            raise ValidationError("Enter a valid email address.")

        if "." not in domain:
            raise ValidationError("Enter a valid email address.")
        return email

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock']

class CustomFileInput(forms.ClearableFileInput):
    template_name = 'widgets/custom_file_input.html'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'birthdate', 'avatar']
        widgets = {
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
            raise forms.ValidationError("Birthdate is required.")

        today = datetime.date.today()
        age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
        )
        if age < 16:
            raise forms.ValidationError("You must be at least 16 years old to use GoodBite")

        return birthdate
