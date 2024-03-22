import requests, xmltodict, datetime
from django.conf import settings

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

  # Icon based on time per 6 hours
  current_hour = int(datetime.datetime.now().strftime("%H"))
  icon_index = int(current_hour/6)

  # Area
  areas = parse['data']['forecast']['area']
  climate = []
  for index, area in enumerate(areas):
    data = {}
    data['index'] = index
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


def get_wilayah_detail(index1: int, index2: int):
  response = requests.get(index1)
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
  timestamp = f'{year}-{month}-{day} {hour}:{minute}:{second}'

  # Area
  areas = parse['data']['forecast']['area']
  area = areas[index2]
  city = area['name'][1]['#text']

  # Geo-coordinate
  longitude = convert_dd_to_dms(float(area['@latitude']), 'latitude')
  latitude = convert_dd_to_dms(float(area['@longitude']), 'longitude')
  
  # Return the data
  humidity = []
  max_humidity = []
  min_humidity = []
  weather = []
  temperature = []
  max_temperature = []
  min_temperature = []
  wind_speed = []
  wind_direction = []


  for item in area['parameter']:
    for index, timerange in enumerate(item['timerange']):
      data = {}
      parameter = item['@description']

      try:
        tr_datetime = timerange['@h']
      except:
        tr_datetime = timerange['@day']
    
      if parameter == 'Humidity':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = tr_datetime
        data['value'] = timerange['value']['#text']
        data['unit'] = timerange['value']['@unit']
        humidity.append(data)
      elif parameter == 'Max humidity':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = f'{tr_datetime[:4]}-{tr_datetime[4:6]}-{tr_datetime[6:]}'
        data['value'] = timerange['value']['#text']
        data['unit'] = timerange['value']['@unit']
        max_humidity.append(data)
      elif parameter == 'Min humidity':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = f'{tr_datetime[:4]}-{tr_datetime[4:6]}-{tr_datetime[6:]}'
        data['value'] = timerange['value']['#text']
        data['unit'] = timerange['value']['@unit']
        min_humidity.append(data)
      elif parameter == 'Weather':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = tr_datetime
        data['unit'] = timerange['value']['@unit']
        data['value'] = timerange['value']['#text']

        if timerange['value']['#text'] == '0': 
          data['label'] = 'Cerah' #'Clear Skies'
        elif timerange['value']['#text'] == '1':
          data['label'] = 'Cerah' #'Clear Skies'
        elif timerange['value']['#text'] == '2':
          data['label'] = 'Cerah Berawan' #'Partly Cloudy'
        elif timerange['value']['#text'] == '3':
          data['label'] = 'Berawan' #'Mostly Cloudy'
        elif timerange['value']['#text'] == '4':
          data['label'] = 'Berawan Tebal' #'Overcast'
        elif timerange['value']['#text'] == '5':
          data['label'] = 'Udara Kabur' #'Haze'
        elif timerange['value']['#text'] == '10':
          data['label'] = 'Asap' #'Smoke'
        elif timerange['value']['#text'] == '45':
          data['label'] = 'Kabut' #'Fog'
        elif timerange['value']['#text'] == '60':
          data['label'] = 'Hujan Ringan' #'Light Rain'
        elif timerange['value']['#text'] == '61':
          data['label'] = 'Hujan Sedang' #'Rain'
        elif timerange['value']['#text'] == '63':
          data['label'] = 'Hujan Lebat' #'Heavy Rain'
        elif timerange['value']['#text'] == '80':
          data['label'] = 'Hujan Lokal' #'Isolated Shower'
        elif timerange['value']['#text'] == '95':
          data['label'] = 'Hujan Petir' #'Severe Thunderstorm'
        elif timerange['value']['#text'] == '97':
          data['label'] = 'Hujan Petir' #'Severe Thunderstorm'
        else:
          data['label'] = 'Tidak ada data'
        
        weather.append(data)
      elif parameter == 'Temperature':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = tr_datetime
        data['value'] = timerange['value'][0]['#text']
        data['unit'] = timerange['value'][0]['@unit']
        temperature.append(data)
      elif parameter == 'Max temperature':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = f'{tr_datetime[:4]}-{tr_datetime[4:6]}-{tr_datetime[6:]}'
        data['value'] = timerange['value'][0]['#text']
        data['unit'] = timerange['value'][0]['@unit']
        max_temperature.append(data)
      elif parameter == 'Min temperature':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = f'{tr_datetime[:4]}-{tr_datetime[4:6]}-{tr_datetime[6:]}'
        data['value'] = timerange['value'][0]['#text']
        data['unit'] = timerange['value'][0]['@unit']
        min_temperature.append(data)
      elif parameter  == 'Wind direction':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = tr_datetime
        data['value'] = timerange['value'][0]['#text']
        data['unit'] = timerange['value'][0]['@unit']
        wind_direction.append(data)
      elif parameter == 'Wind speed':
        data['index'] = index
        data['parameter'] = parameter
        data['datetime'] = tr_datetime
        data['value'] = timerange['value'][2]['#text']
        data['unit'] = timerange['value'][2]['@unit']
        wind_speed.append(data)

  # import json
  # with open(f'{settings.MEDIA_ROOT}/temp/humidity.json', 'w') as file:
  #   json.dump(humidity, file)

  return {
    'city': city,
    'source': source,
    'timestamp': timestamp,
    'longitude': longitude,
    'latitude': latitude,
    'weather': weather,
    'wind_speed': wind_speed,
    'wind_direction': wind_direction,
    'humidity': humidity,
    'max_humidity': max_humidity,
    'min_humidity': min_humidity,
    'temperature': temperature,
    'max_temperature': max_temperature,
    'min_temperature': min_temperature,
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
