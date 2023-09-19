from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model  = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password dont match.')
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'birthday']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.get('initial', {})
        if 'instance' in kwargs:
            instance = kwargs['instance']
            initial_data['avatar'] = instance.avatar.url if instance.avatar else ''
        kwargs['initial'] = initial_data
        super().__init__(*args, **kwargs)
