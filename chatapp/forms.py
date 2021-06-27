from django.contrib.auth.models import User
from django import forms
from .models import Profile

class Profileform(forms.ModelForm):
    class Meta:
        model=Profile

        fields=['profile_image']

class Userform(forms.ModelForm):
    class Meta:
        model=User

        fields=['username','email','password']