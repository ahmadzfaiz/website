from django.shortcuts import render
from home.signals import log_activity

# Create your views here.
def blog(request):
  if request.method == 'GET':
    log_activity(request)

  return render(request, 'blog/blog.html')