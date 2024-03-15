from django.shortcuts import render
from django.views.generic import TemplateView
from .pipelines import get_wilayah, get_cuaca_api, list_cuaca_api

# Create your views here.
class HomeView(TemplateView):
  template_name = 'iklim/home.html'

  def get(self, request, *args, **kwargs):
    data = get_wilayah('https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Indonesia.xml')

    context = {
      'data': data,
      'provinsi': list_cuaca_api
    }
    return render(request, self.template_name, context=context)


class MainView(TemplateView):
  template_name = 'iklim/main.html'

  def get(self, request, index):
    cuaca_api = get_cuaca_api(index)
    data = get_wilayah(cuaca_api['url'])
    page = cuaca_api['page']

    context = {
      'data': data,
      'page': page,
      'provinsi': list_cuaca_api
    }
    return render(request, self.template_name, context=context)