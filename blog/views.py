from django.shortcuts import render
from home.signals import log_activity
from blog.forms import UserRegistration
from blog.models import post

# Create your views here.
def blog(request):
  if request.method == 'GET':
    log_activity(request)

  posts = post.objects.all()

  context = {
    'post': posts
  }

  return render(request, 'blog/blog.html', context)

def register(request):
  if request.method == 'POST':
    user_form = UserRegistration(request.POST)

    if user_form.is_valid():
      new_user = user_form.save(commit=False)
      new_user.set_password(user_form.cleaned_data['password'])
      new_user.save()
      return render(request, 'account/register_done.html', {'user_form': user_form})
    
  else:
    user_form = UserRegistration()

  return render(request, 'account/register.html', {'user_form': user_form})