from django.shortcuts import render, redirect
from home.models import Experience, Certificate, Skill, Contact
from home.forms import contactForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def home(request):
  exp = Experience.objects.all
  cert = Certificate.objects.all
  skill = Skill.objects.all
  contact = Contact.objects.all

  if request.method == 'POST':
    contact = contactForm(request.POST)
    if contact.is_valid():
      item = contact.save(commit= False)
      item.user = request.user
      item.save()

      html = render_to_string('home/email.html', {
        'name': item.name,
        'email': item.email,
        'phone': item.phone_number,
        'message': item.message
      }) 

      sent_to = ['zaenun.faiz@gmail.com', item.email]
      send_mail(item.name, item.message, 'ahmadzfaiz.gcp@gmail.com', sent_to, html_message= html, fail_silently=False)
      return redirect('home')
  
  else:
    contact = contactForm()

  return render(request, 'home/home.html', {
    'skill': skill,
    'certificate': cert,
    'experience': exp,
    'contact': contact,
    'contact': contact 
  })