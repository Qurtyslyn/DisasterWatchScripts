import requests
import json


#Setup Output file
output_file = "/var/www/DisasterWatch/NWS.geojson"

#GeoJSON Files
coastalJSON = "./NWSCoastalZones.geojson"
zonesJSON = "./NWSZones.geojson"

#Load local GeoJSON files
with open(coastalJSON, 'r') as file:
    coastalData = json.load(file)

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#Combine Zones
coastalData['features'] = coastalData['features'] + zonesData['features']

zones = coastalData

#print(zones['features'][0]['properties']['ID'])

#Load Data from NWS
NWSURL = 'https://api.weather.gov/alerts/active?status=actual'

response = requests.get(NWSURL)

response.raise_for_status()

nwsData = response.json()

for feature in nwsData["features"]:
    if feature['geometry'] is None:
        geocode = feature['properties']['geocode']["UGC"]

        if len(geocode) == 1:
            
            for item in zones['features']:
                ID = item['properties']['ID']
                
                if geocode[0] == ID:
                   #print(item['properties']['ID'])
                   feature['geometry'] = item['geometry']
                #break
            #feature['geometry'] = next((item['geometry'] for item in zones['features'] if item['properties']['ID'] == geocode),None)
            #print(feature['geometry'])


#print(json.dumps(nwsData, indent=4))

with open(output_file, 'w') as file:
    json.dump(nwsData, file)