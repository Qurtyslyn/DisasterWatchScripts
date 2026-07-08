import requests
import json
import gc
import sys
from collections import Counter

def checkPolygonDepth(lst):
    if  not isinstance(lst, list):
        return 0
    elif isinstance(lst, list) and not isinstance(lst[0], list):
        return 1
    elif isinstance(lst, list) and isinstance(lst[0], list) and not isinstance(lst[0][0], list):
        return 2
    else:
        return 3

#Setup Output file
output_file = "/var/www/DisasterWatch/NWS.geojson"

#GeoJSON Files
#zonesJSON = "./Zones.geojson"
zonesJSON = "/home/curtis/DisasterWatchScripts/Zones.geojson"

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

#print(list( (Counter(zoneNeeded)-Counter(coordinateDict.keys())).elements()))

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

        

        for zone in geocode:
            coordList = []
            if zone in coordinateDict.keys():
                #if len(coordinateDict[zone]['coordinates']) > 1:
                    #print("Index: " + str(index))
                    #print("Length: " + str(len(coordinateDict[zone]['coordinates'])))

                for polygon in coordinateDict[zone]['coordinates']:
                    if len(coordinateDict[zone]['coordinates']) > 1:
                        #placeholder
                        temp = 1

                        # for subPoly in polygon:
                        #     #print("Depth: " + str(checkPolygonDepth(subPoly)))
                        #     if checkPolygonDepth(subPoly) == 2:
                                
                        #         container = []
                        #         container.append(subPoly)
                        #         coordList.append(container)
                                
                        #     if isinstance(subPoly, list):
                        #         for triPoly in subPoly:
                        #             coordList.append(triPoly)
                        #     else:
                        #         coordList.append(subPoly)
                    else:
                    #nwsData['features'][index]['geometry']['coordinates'].append(polygon)
                        #print("Needed Depth: " + str(checkPolygonDepth(polygon)))
                        coordList.append(polygon)
                    #print("Polygon: " + str(len(polygon)))

            nwsData['features'][index]['geometry']['coordinates'].append(coordList)
        #print(index)




with open(output_file, 'w') as file:
    json.dump(nwsData, file)