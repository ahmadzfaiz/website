from django.shortcuts import render, redirect
from home.models import Experience, Skill, Contact
from home.forms import contactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def home(request):
  exp = Experience.objects.all
  skill = Skill.objects.all
  contact = Contact.objects.all

  if request.method == 'POST':
    contact = contactForm(request.POST)
    if contact.is_valid():
      item = contact.save(commit= False)
      item.user = request.user
      item.save()

      from_email = settings.DEFAULT_FROM_EMAIL  

      html = render_to_string('home/email.html', {
        'name': item.name,
        'email': item.email,
        'phone': item.phone_number,
        'message': item.message
      })  # html_message= html, 

      send_mail(item.name, item.message, from_email, [item.email], html_message= html, fail_silently=False)
      return redirect('home')
  
  else:
    contact = contactForm()

  return render(request, 'home/home.html', {
    'skill': skill,
    'experience': exp,
    'contact': contact,
    'contact': contact 
  })