from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Portfolio, Experience, Certificate, Skill, Contact, YoutubeVideos
from .forms import contactForm
from .signals import log_activity


def home(request):
    if request.method == 'GET':
        log_activity(request)

    port = Portfolio.objects.all
    exp = Experience.objects.all
    cert = Certificate.objects.all
    skill = Skill.objects.all
    contact = Contact.objects.all
    youtube = YoutubeVideos.objects.all

    if request.method == 'POST':
        contact = contactForm(request.POST)

        if contact.is_valid():
            item = contact.save(commit=False)
            item.user = request.user
            item.save()

            html = render_to_string('home/email.html', {
                'name': item.name,
                'email': item.email,
                'phone': item.phone_number,
                'message': item.message,
            })

            sent_to = [item.email, 'ahmadzfaiz.gcp@gmail.com']
            send_mail(item.name, item.message, 'ahmadzfaiz.gcp@gmail.com', sent_to, html_message=html, fail_silently=False)
            return redirect('home')

    else:
        contact = contactForm()

    return render(request, 'home/home.html', {
        'portfolio': port,
        'skill': skill,
        'certificate': cert,
        'experience': exp,
        'contact': contact,
        'youtube': youtube,
    })
