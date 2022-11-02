from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import User

class createuserform(UserCreationForm):
    class Meta:
        model= User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]