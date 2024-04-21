import json, requests, os, math
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
import numpy as np

class HomeView(TemplateView):
  def get(self, request, *args, **kwargs):
    facet_list = [
      'publishing_country',
      'basis_of_record',
      'kingdom_key'
    ]

    facets = ''
    for index, facet in enumerate(facet_list):
      if index == 0:
        facets = f'facet={facet}'
      else:
        facets = facets + f'&facet={facet}'
      
    get_statistics = requests.get(f'https://www.gbif.org/api/occurrence/search?{facets}', {
      'limit': 0,
      'facetLimit': 500,
      'country': 'ID'
    })

    def symbol_config(icon, color):
      return {'icon': icon, 'color': color}

    kingdom_settings = [
      symbol_config('https://www.svgrepo.com/show/361407/workspace-unknown.svg', 'orange'),
      symbol_config('https://www.svgrepo.com/show/404229/tiger.svg', 'red'),
      symbol_config('https://www.svgrepo.com/show/418317/cell-chromatids-chromosome.svg', 'pink'),
      symbol_config('https://www.svgrepo.com/show/482874/bacteria-2.svg', 'blue'),
      symbol_config('https://www.svgrepo.com/show/201550/bacteria.svg', 'purple'),
      symbol_config('https://www.svgrepo.com/show/298870/mushroom.svg', 'yellow'),
      symbol_config('https://www.svgrepo.com/show/209879/maple-leaf-season.svg', 'green'),
      symbol_config('https://www.svgrepo.com/show/200954/bacteria.svg', 'aquamarine'),
      symbol_config('https://www.svgrepo.com/show/452669/virus.svg', 'black'),
    ]

    bor_settings = [
      symbol_config('https://www.svgrepo.com/show/414064/preserve.svg', 'blue'),
      symbol_config('https://www.svgrepo.com/show/322568/human-target.svg', 'orange'),
      symbol_config('https://www.svgrepo.com/show/429885/flask-sample-test.svg', 'red'),
      symbol_config('https://www.svgrepo.com/show/508979/vc-fossil.svg', 'green'),
      symbol_config('https://www.svgrepo.com/show/452875/bird.svg', 'purple'),
      symbol_config('https://www.svgrepo.com/show/11631/plant-sample.svg', 'aquamarine'),
      symbol_config('https://www.svgrepo.com/show/89864/open-book.svg', 'black'),
      symbol_config('https://www.svgrepo.com/show/340628/machine-learning-model.svg', 'yellow'),
      symbol_config('https://www.svgrepo.com/show/410573/observe.svg', 'pink'),
    ]

    statistics = json.loads(get_statistics.text)['facets']
    params = {
      'bor': statistics['BASIS_OF_RECORD']['counts'].items(),
      'bor_settings': bor_settings,
      'country': statistics['PUBLISHING_COUNTRY']['counts'],
      'kingdom': statistics['KINGDOM_KEY']['counts'].items(),
      'kingdom_settings': kingdom_settings
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
    response = requests.get(f'https://api.gbif.org/v1/occurrence/{page}')
    data = json.loads(response.text)
    params = {
      'data': data
    }
    return render(request, 'biodiversity/detail_pengamatan.html', params)