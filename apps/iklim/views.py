import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from bs4 import BeautifulSoup
from .pipelines import get_wilayah

# Create your views here.
# class MainView(TemplateView):
#   template_name = 'iklim/main.html'

#   def get(self, request, *args, **kwargs):
#     html_doc = requests.get('https://data.bmkg.go.id/prakiraan-cuaca/').content
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     data = [item.a['href'].replace('../', 'https://data.bmkg.go.id/') for item in soup.find_all('pre') if item.a is not None]
#     context = {
#       'soup': data
#     }
#     return render(request, self.template_name, context=context)
  
class MainView(TemplateView):
  template_name = 'iklim/main.html'

  def get(self, request, *args, **kwargs):
    context = get_wilayah('https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Indonesia.xml')
    return render(request, self.template_name, context=context)