import requests, xmltodict, datetime

def convert_dd_to_dms(degrees, type):
  """
  Convert decimal degrees (DD) to degrees, minutes, and seconds (DMS).

  Parameters:
  degrees (float): The decimal degrees to be converted.

  Returns:
  str: The degrees, minutes, and seconds in DMS format.

  Example:
  >>> convert_dd_to_dms(45.6789)
  '45°40'44.04"LS'
  """

  # Get the integer part of the degrees
  degrees_int = int(degrees)

  # Get the decimal part of the degrees
  degrees_decimal = degrees - degrees_int

  # Convert the decimal part to minutes
  minutes = degrees_decimal * 60

  # Get the integer part of the minutes
  minutes_int = int(minutes)

  # Get the decimal part of the minutes
  minutes_decimal = minutes - minutes_int

  # Convert the decimal part to seconds
  seconds = minutes_decimal * 60

  # Setup type
  if type == 'longitude':
    if degrees >= 0:
      suffix = 'BT'
    else:
      suffix = 'BB'

  elif type == 'latitude':
    if degrees >= 0:
      suffix = 'LU'
    else:
      suffix = 'LS'

  else:
    suffix = 'NA'

  # Format the DMS string
  dms = f"{abs(degrees_int)}°{abs(minutes_int)}'{abs(seconds):.2f}\"{suffix}"

  return dms


def get_wilayah(url):
  response = requests.get(url)
  parse = xmltodict.parse(response.text)

  # Data source
  source = parse['data']['@source']

  # Issued timestamp
  year = parse['data']['forecast']['issue']['year']
  month = parse['data']['forecast']['issue']['month']
  day = parse['data']['forecast']['issue']['day']
  hour = parse['data']['forecast']['issue']['hour']
  minute = parse['data']['forecast']['issue']['minute']
  second = parse['data']['forecast']['issue']['second']
  timestamp = f'{year}-{month}-{day} {hour}:{minute}:{second} WIB'

  # Icon based on time per 3 hours
  current_hour = int(datetime.datetime.now().strftime("%H"))
  icon_index = int(current_hour/3)

  # Area
  areas = parse['data']['forecast']['area']
  climate = []
  for area in areas:
    data = {}
    data['lat'] = convert_dd_to_dms(float(area['@latitude']), 'latitude')
    data['lon'] = convert_dd_to_dms(float(area['@longitude']), 'longitude')
    
    if area['@type'] == 'land':
      data['name'] = area['name'][1]['#text']
    else:
      data['name'] = area['@description']

    try:
      data['icon'] = area['parameter'][6]['timerange'][icon_index]['value']['#text']
    except:
      data['icon'] = 'no_data'

    if data['icon'] == '0': 
      data['weather'] = 'Cerah' #'Clear Skies'
    elif data['icon'] == '1':
      data['weather'] = 'Cerah' #'Clear Skies'
    elif data['icon'] == '2':
      data['weather'] = 'Cerah Berawan' #'Partly Cloudy'
    elif data['icon'] == '3':
      data['weather'] = 'Berawan' #'Mostly Cloudy'
    elif data['icon'] == '4':
      data['weather'] = 'Berawan Tebal' #'Overcast'
    elif data['icon'] == '5':
      data['weather'] = 'Udara Kabur' #'Haze'
    elif data['icon'] == '10':
      data['weather'] = 'Asap' #'Smoke'
    elif data['icon'] == '45':
      data['weather'] = 'Kabut' #'Fog'
    elif data['icon'] == '60':
      data['weather'] = 'Hujan Ringan' #'Light Rain'
    elif data['icon'] == '61':
      data['weather'] = 'Hujan Sedang' #'Rain'
    elif data['icon'] == '63':
      data['weather'] = 'Hujan Lebat' #'Heavy Rain'
    elif data['icon'] == '80':
      data['weather'] = 'Hujan Lokal' #'Isolated Shower'
    elif data['icon'] == '95':
      data['weather'] = 'Hujan Petir' #'Severe Thunderstorm'
    elif data['icon'] == '97':
      data['weather'] = 'Hujan Petir' #'Severe Thunderstorm'
    else:
      data['weather'] = 'Tidak ada data'
    climate.append(data)

  return {
    'source': source,
    'timestamp': timestamp,
    'climate': climate
  }

list_cuaca_api = [
  {'title': 'Daerah Istimewa Yogyakarta', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DIYogyakarta.xml'}, 
  {'title': 'Daerah Khusus Ibukota Jakarta', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml'}, 
  {'title': 'Provinsi Aceh', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml'}, 
  {'title': 'Provinsi Bali', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Bali.xml'}, 
  {'title': 'Provinsi Bangka Belitung', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-BangkaBelitung.xml'}, 
  {'title': 'Provinsi Banten', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Banten.xml'}, 
  {'title': 'Provinsi Bengkulu', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Bengkulu.xml'}, 
  {'title': 'Provinsi Gorontalo', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Gorontalo.xml'}, 
  {'title': 'Provinsi Jambi', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Jambi.xml'}, 
  {'title': 'Provinsi Jawa Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml'}, 
  {'title': 'Provinsi Jawa Tengah', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml'}, 
  {'title': 'Provinsi Jawa Timur', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml'}, 
  {'title': 'Provinsi Kalimantan Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanBarat.xml'}, 
  {'title': 'Provinsi Kalimantan Selatan', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanSelatan.xml'}, 
  {'title': 'Provinsi Kalimantan Tengah', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanTengah.xml'}, 
  {'title': 'Provinsi Kalimantan Timur', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanTimur.xml'}, 
  {'title': 'Provinsi Kalimantan Utara', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanUtara.xml'}, 
  {'title': 'Provinsi Kepulauan Riau', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KepulauanRiau.xml'}, 
  {'title': 'Provinsi Lampung', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Lampung.xml'}, 
  {'title': 'Provinsi Maluku', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Maluku.xml'}, 
  {'title': 'Provinsi Maluku Utara', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-MalukuUtara.xml'}, 
  {'title': 'Provinsi Nusa Tenggara Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraBarat.xml'}, 
  {'title': 'Provinsi Nusa Tenggara Timur', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraTimur.xml'}, 
  {'title': 'Provinsi Papua', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Papua.xml'}, 
  {'title': 'Provinsi Papua Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-PapuaBarat.xml'}, 
  {'title': 'Provinsi Riau', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Riau.xml'}, 
  {'title': 'Provinsi Sulawesi Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiBarat.xml'}, 
  {'title': 'Provinsi Sulawesi Selatan', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiSelatan.xml'}, 
  {'title': 'Provinsi Sulawesi Tengah', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiTengah.xml'}, 
  {'title': 'Provinsi Sulawesi Tenggara', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiTenggara.xml'}, 
  {'title': 'Provinsi Sulawesi Utara', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiUtara.xml'}, 
  {'title': 'Provinsi Sumatera Barat', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraBarat.xml'}, 
  {'title': 'Provinsi Sumatera Selatan', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraSelatan.xml'}, 
  {'title': 'Provinsi Sumatera Utara', 'url': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraUtara.xml'}, 
]

def get_cuaca_api(index:int):
  data = list_cuaca_api

  next_data = index + 1
  if next_data > len(data) - 1:
    next_data = len(data) - 1
  
  previous_data = index - 1
  if previous_data < 0:
    previous_data = 0
  
  results = {
    'data': data,
    'url': data[index]['url'],
    'page': {
      'title': data[index]['title'],
      'index': index,
      'next': next_data,
      'previous': previous_data,
      'first': 0,
      'last': len(data) - 1
    }
  }
  return results