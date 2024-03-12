from django import forms
from apps.home.models import Contact
from captcha.fields import ReCaptchaField

class contactForm(forms.ModelForm):
  captcha = ReCaptchaField()

  class Meta:
    model = Contact
    fields = ('name', 'email', 'phone_number', 'message')