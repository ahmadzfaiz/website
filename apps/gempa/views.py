import requests, json
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# def test(request):
#   return render(request, 'gempa/test.html', {})

class HomeView(TemplateView):
  def get(self, request, *args, **kwargs):
    response = requests.get('https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json')
    parse = json.loads(response.text)
    parse['Infogempa']['gempa']['Dirasakan'] = parse['Infogempa']['gempa']['Dirasakan'].split(', ')

    params = {
      'data': parse
    }
    return render(request, 'gempa/home.html', params)