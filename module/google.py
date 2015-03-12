# -*-coding:UTF-8 -*
import json
import urllib.request
import datetime
import time
import urllib.parse

geoloc_addr = "https://maps.googleapis.com/maps/api/geocode/json?language=fr&"
timez_addr = "https://maps.googleapis.com/maps/api/timezone/json?language=fr&"

print("---- google module loaded ----")

def get_geoloc(address):
    query = "address="+urllib.parse.quote('+'.join(address.split(' ')))
    try:
        data_j = urllib.request.urlopen(geoloc_addr+query).read().decode()
        data = json.loads(data_j)['results'][0]
    except:
        print("*** erreur geoloc ***")
        return 0,0,'-1'
    geoloc = data['geometry']['location']
    return geoloc['lat'], geoloc['lng'], data['formatted_address']
    
def get_time_by_geoloc(address = "Paris"):
    lat, lng, name = get_geoloc(address)
    if name == '-1':
        return  'Lieu introuvable', '-', '-', '-', '-'
    query = "location="+str(lat)+","+str(lng)+"&timestamp="+str(time.time())
    try:
        data_j = urllib.request.urlopen(timez_addr+query).read().decode()
        data = json.loads(data_j)
    except:
        print("*** erreur time zone ***")
        return  'Lieu introuvable', '-', '-', '-', '-'
    timezone = datetime.timezone(datetime.timedelta(seconds=data['rawOffset']), data['timeZoneId'])
    dt = datetime.datetime.now(timezone)
    return name, dt.hour, dt.minute, dt.second, data['timeZoneName']
