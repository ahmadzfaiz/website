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
    data['name'] = area['name'][1]['#text']
    data['icon'] = area['parameter'][6]['timerange'][icon_index]['value']['#text']

    if data['icon'] == '0': 
      data['weather'] = 'Cerah / Clear Skies'
    elif data['icon'] == '1':
      data['weather'] = 'Cerah / Clear Skies'
    elif data['icon'] == '2':
      data['weather'] = 'Cerah Berawan / Partly Cloudy'
    elif data['icon'] == '3':
      data['weather'] = 'Berawan / Mostly Cloudy'
    elif data['icon'] == '4':
      data['weather'] = 'Berawan Tebal / Overcast'
    elif data['icon'] == '5':
      data['weather'] = 'Udara Kabur / Haze'
    elif data['icon'] == '10':
      data['weather'] = 'Asap / Smoke'
    elif data['icon'] == '45':
      data['weather'] = 'Kabut / Fog'
    elif data['icon'] == '60':
      data['weather'] = 'Hujan Ringan / Light Rain'
    elif data['icon'] == '61':
      data['weather'] = 'Hujan Sedang / Rain'
    elif data['icon'] == '63':
      data['weather'] = 'Hujan Lebat / Heavy Rain'
    elif data['icon'] == '80':
      data['weather'] = 'Hujan Lokal / Isolated Shower'
    elif data['icon'] == '95':
      data['weather'] = 'Hujan Petir / Severe Thunderstorm'
    elif data['icon'] == '97':
      data['weather'] = 'Hujan Petir / Severe Thunderstorm'
    else:
      data['weather'] = 'Tidak ada data'
    climate.append(data)

  return {
    'source': source,
    'timestamp': timestamp,
    'climate': climate
  }