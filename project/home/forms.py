from django import forms
from django_recaptcha.fields import ReCaptchaField
from .models import Contact


class contactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone_number', 'message')
