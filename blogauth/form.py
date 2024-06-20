from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', min_length=2, max_length=20, error_messages={
        "required": "please enter your username",
        "max_length": "Maximum length of username is 20 characters",
        "min_length": "Minimum length of username is 2 characters",
    })
    email = forms.EmailField(error_messages={'required': 'please enter your email address',
                                             'invalid': 'Please enter an correct email address'})
    captcha = forms.CharField(min_length=4, max_length=4, error_messages={
        'required': 'Please enter your verification code',
        'min_length': 'Minimum length of code is 4 characters',
        'max_length': 'Maximum length of code is 4 characters',
    })
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'required': 'Please enter your password',
        'min_length': 'Minimum length of password is 6 characters',
        'max_length': 'Maximum length of password is 20 characters',
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("Email already registered")
        else:
            return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("Verification code does not match your email")
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': 'please enter your email address',
                                             'invalid': 'Please enter an correct email address'})
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'required': 'Please enter your password',
        'min_length': 'Minimum length of password is 6 characters',
        'max_length': 'Maximum length of password is 20 characters',
    })

    remember = forms.IntegerField(required=False)
