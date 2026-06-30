import requests
import json
import gc
import sys
from collections import Counter

#Setup Output file
output_file = "/var/www/DisasterWatch/NWS.geojson"

#GeoJSON Files
zonesJSON = "./Zones.geojson"
#zonesJSON = "/home/curtis/DisasterWatchScripts/Zones.geojson"

#Load local GeoJSON files
with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#Load Data from NWS
NWSURL = 'https://api.weather.gov/alerts/active?status=actual'

response = requests.get(NWSURL)

response.raise_for_status()

nwsData = response.json()

#Loop through alerts and find Empty Geometries to speed up future loops
#Get list of Zones needed for polygons
entry = 0
emptyGeoEntry = []
zoneNeeded = []

for feature in nwsData['features']:
    if feature['geometry'] is None:
        emptyGeoEntry.append(entry)

        if 'UGC' not in feature['properties']['geocode'].keys():
            continue

        for ID in feature['properties']['geocode']["UGC"]:
            if ID not in zoneNeeded:
                zoneNeeded.append(ID)
        
    entry = entry + 1

#Create a dict for coordinates for geometries to fill in empty ones
coordinateDict = {}

#Loop through zones and add geometries to Dcit
for feature in zonesData['features']:
    if feature['properties']['ID'] in zoneNeeded:
        coordinateDict[feature['properties']['ID']] = feature['geometry']

#Destroy zonesData variable to free up memory
del zonesData
gc.collect()

print(list( (Counter(zoneNeeded)-Counter(coordinateDict.keys())).elements()))

#Loop through only empty Geometries and fill in from CoordinateDict
for index in emptyGeoEntry:
    if 'UGC' not in nwsData['features'][index]['properties']['geocode'].keys():
            continue
    
    geocode = nwsData['features'][index]['properties']['geocode']["UGC"]

    #If Alert only covers one zone
    if len(geocode) == 1:
        if geocode[0] in coordinateDict.keys():
            nwsData['features'][index]['geometry'] = coordinateDict[geocode[0]]
    #If Alert covers more than one zone, change geometry type to MultiPolygon and attach additional zones to Geometry
    else:
        nwsData['features'][index]['geometry'] = {}

        nwsData['features'][index]['geometry']['type'] = "MultiPolygon"

        nwsData['features'][index]['geometry']['coordinates'] = []

        coordList = []

        for zone in geocode:
            if zone in coordinateDict.keys():
                for polygon in coordinateDict[zone]['coordinates']:
                    #nwsData['features'][index]['geometry']['coordinates'].append(polygon)
                    coordList.append(polygon)

        nwsData['features'][index]['geometry']['coordinates'].append(coordList)
        print(index)
        break




with open(output_file, 'w') as file:
    json.dump(nwsData, file)