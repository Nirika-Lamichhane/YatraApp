from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta: # meta class is the inherent fixed class that django uses to define the model and fields for the form
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'profile_photo', 'citizenship_number','role', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1') # self
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")

        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("Password must contain at least one special character (!@#$ etc).")

        return password2

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits!")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone
    
    def clean_citizenship_number(self):
        citizenship=self.cleaned_data.get('citizenship_number')
        role= self.cleaned_data.get('role')
        if role=='guide':
            if not citizenship:
                raise ValidationError("Citizenship number is required for tour guides.")
            if not re.match(r'^\d{6,12}$', citizenship):  
                # ^ and $ make sure nothing else is added before and after the number

                raise ValidationError("Enter valid citizenship number.")
        return citizenship


    def clean(self):
        cleaned_data = super().clean()
        profile_photo = cleaned_data.get("profile_photo")

        if not profile_photo :
            raise ValidationError("Profile Photo must be uploaded.")

    
        if profile_photo.size > 2 * 1024 * 1024:
            raise ValidationError("Each photo must be less than 2MB.")
        if not profile_photo.content_type in ['image/jpeg', 'image/png']:
            raise ValidationError("Only JPEG and PNG images are allowed.")

        return cleaned_data
