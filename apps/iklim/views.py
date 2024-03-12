from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import requests, xmltodict, datetime

# Create your views here.
def convert_dd_to_dms(degrees, type):
  """
  Convert decimal degrees (DD) to degrees, minutes, and seconds (DMS).

  Parameters:
  degrees (float): The decimal degrees to be converted.

  Returns:
  str: The degrees, minutes, and seconds in DMS format.

  Example:
  >>> convert_dd_to_dms(45.6789)
  '45° 40' 44.04"'
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
  dms = f"{degrees_int}°{minutes_int}'{seconds:.2f}\"{suffix}"

  return dms

class MainView(TemplateView):
  template_name = 'iklim/main.html'

  def get(self, request, *args, **kwargs):
    response = requests.get('https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml')
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

    # Area
    areas = parse['data']['forecast']['area']
    climate = []
    for area in areas:
      data = {}
      data['lat'] = convert_dd_to_dms(float(area['@latitude']), 'latitude')
      data['lon'] = convert_dd_to_dms(float(area['@longitude']), 'longitude')
      data['name'] = area['name'][1]['#text']
      climate.append(data)

    context = {
      'source': source,
      'timestamp': timestamp,
      'climate': climate,
    }
    return render(request, self.template_name, context=context)