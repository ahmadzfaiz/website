from django.shortcuts import render
from .models import Experience, Skill

# Create your views here.
def home(request):
  exp = Experience.objects.all
  skill = Skill.objects.all
  return render(request, 'home/home.html', {
    'skill': skill,
    'experience': exp,
  })