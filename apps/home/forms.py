from django import forms
from apps.home.models import Contact
from django_recaptcha.fields import ReCaptchaField

class contactForm(forms.ModelForm):
  captcha = ReCaptchaField()

  class Meta:
    model = Contact
    fields = ('name', 'email', 'phone_number', 'message')