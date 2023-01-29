from django import forms
from home.models import Contact

class contactForm(forms.ModelForm):
  class Meta:
    model = Contact
    fields = ('name', 'email', 'phone_number', 'message')