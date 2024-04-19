import json, requests, os, math
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
import numpy as np

# Create your views here.
class HomeView(TemplateView):
  def get(self, request, *args, **kwargs):
    params = {
      'data': 'data'
    }
    return render(request, 'biodiversity/home.html', params)
  
class PengamatanView(TemplateView):
  def get(self, request, page):
    with open(os.path.join(settings.BASE_DIR, 'apps/biodiversity/data/gbif.json')) as file:
      file = json.load(file)

    data_count = len(file)
    page_count = math.ceil(data_count / 10)

    page_start = (page - 1) * 10
    page_end = page * 10
    list_data = file[page_start:page_end]

    data = np.array([])
    session = requests.Session()
    for item in list_data:
      response = session.get(f'https://api.gbif.org/v1/occurrence/{item}')
      data = np.append(data, json.loads(response.text))

    params = {
      'count': page_count,
      'data': data,
      'page': page
    }
    return render(request, 'biodiversity/daftar_pengamatan.html', params)
  
  def post(self, request, page):
    data = request.POST
    action = data.get('page')
    return redirect('biodiversity_pengamatan', action)
  
class DetailPengamatanView(TemplateView):
  def get(self, request, page):
    params = {
      'data': 'data'
    }
    return render(request, 'biodiversity/home.html', params)