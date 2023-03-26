from django import forms
from home.models import Contact
from captcha.fields import ReCaptchaField

class contactForm(forms.ModelForm):
  captcha = ReCaptchaField()

  class Meta:
    model = Contact
    fields = ('name', 'email', 'phone_number', 'message')