from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.safestring import mark_safe
#from django import ModelForm
from core.models import User


class createuserform(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super(createuserform,self).__init__(*args,**kwargs)

    email=forms.EmailField(widget=forms.TextInput(
        attrs={'class':'form-control','id':'id_email','placeholder':'Email...'}
    ))
    username=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','id':'id_username','placeholder':'Name...'}
    ))
    password1=forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','id':'id_password1','placeholder':'Password...'}
    ))
    password2=forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','id':'id_password2','placeholder':'Password...'}
    ))
    mode = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices= [
            ('S', 'SELLER'),
            ('B', 'BUYER'),
        ], 
    )
    class Meta:
        model= User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'mode'
        ]


# class UserProfileForm(ModelForm):
#     class Meta:
#         model = User
#         fields = []