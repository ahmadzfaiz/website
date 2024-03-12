from django.shortcuts import render, get_object_or_404
from apps.home.signals import log_activity
from apps.blog.forms import UserRegistration
from apps.blog.models import post

# Create your views here.
def home(request):
  if request.method == 'GET':
    log_activity(request)

  article = post.objects.all().order_by('-updated_at')[:5]
  
  context = {
    'article': article
  }
  return render(request, 'blog/home.html', context)

def article(request):
  if request.method == 'GET':
    log_activity(request)

  posts = post.objects.all()

  context = {
    'post': posts
  }
  return render(request, 'blog/article.html', context)

def article_post(request, pk):
  if request.method == 'GET':
    log_activity(request)

  article = get_object_or_404(post, id=pk)
  
  context = {
    'article': article
  }
  return render(request, 'blog/article_post.html', context)

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