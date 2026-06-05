import requests
import json
import xml.etree.ElementTree as ET
import io
import zipfile
import re

#Setup Output file
output_file = "/var/www/DisasterWatch/Hurricanes.geojson"

#Function to extract KML data from KMZ file
def extractKMLData(kmz):
    with zipfile.ZipFile(io.BytesIO(kmz), 'r') as kmz_file:
        filename = next((item for item in kmz_file.namelist() if ".kml" in item), None)

        with kmz_file.open(filename) as kml_file:
            return kml_file.read().decode('utf-8')
        
#Extract a 2-Dimensional List from a comma separated string of coordinates
def getPolygonArray(str):
    #Split the list and remove the extra "0 " in the longitudes
    #flatlist = str.replace("0 ", "").split(",")
    flatlist = re.sub(r"[ \n]", "", str.replace("0 ", "")).split(",")


    #Reshape the list into a 2-Dimensional List
    coordinateList = list(zip(flatlist[::2], flatlist[1::2]))

    return coordinateList

def removeNamespaces(xml):
    #Remove Namespaces from tags
    for element in xml.iter():
        if element.tag.startswith("{"):
            element.tag = element.tag.split("}",1)[1]

            for key in list(element.attrib.keys()):
                if key.startswith("{"):
                    new_key = key.split("}",1)[1]
                    element.attrib[new_key] = element.attrib.pop(key)
    
    return xml

#Download initial KML File and parse to get each Hurricane
#url = "https://www.nhc.noaa.gov/gis/kml/nhc_active.kml"
#response = requests.get(url)

#response.raise_for_status()

#Setup XML Tree for parsing
#kmlRoot = removeNamespaces(ET.fromstring(response.content))

#For Local Testing
tree = ET.parse("/home/curtis/Downloads/nhc_active(1).kml")
kmlRoot = removeNamespaces(tree.getroot())

#Remove Namespaces from tags
# for element in kmlRoot.iter():
#     if element.tag.startswith("{"):
#         element.tag = element.tag.split("}",1)[1]

#         for key in list(element.attrib.keys()):
#             if key.startswith("{"):
#                 new_key = key.split("}",1)[1]
#                 element.attrib[new_key] = element.attrib.pop(key)

#Create GeoJSON variable to store relevant data in
geojson = {"type": "FeatureCollection", "features": []}

#For each hurricane, get the Data and download the follwing
#KMZ files to be unzipped
#Best Track
#Cone of Uncertainty
#Predicted Track
#Extent of Winds
for folder in kmlRoot.findall(".//Document/Folder"):
    if folder.get('id') == "wsp":
        continue

    #Get data from KML
    name = folder.find("name").text
    lat = folder.find("ExtendedData/Data[@name='centerLat']/value").text
    lon = folder.find("ExtendedData/Data[@name='centerLon']/value").text
    dateTime = folder.find("ExtendedData/Data[@name='dateTime']/value").text
    movement = folder.find("ExtendedData/Data[@name='movement']/value").text
    minimumPressure = folder.find("ExtendedData/Data[@name='minimumPressure']/value").text
    maxSustainedWind = folder.find("ExtendedData/Data[@name='maxSustainedWind']/value").text

    #Get Past Track

    #Get Cone of Uncertainty
    coneURL = folder.find("NetworkLink[@id='cone']/Link/href").text
    response = requests.get(coneURL)

    response.raise_for_status()

    coneKML = extractKMLData(response.content)
    coneRoot = removeNamespaces(ET.fromstring(coneKML))
    
    conePolygon = getPolygonArray(coneRoot.find("Document/Placemark/Polygon/outerBoundaryIs/LinearRing/coordinates").text)

    feature = {
        "type": "Feature",
         "geometry": {
            "type": "Polygon", "coordinates": [conePolygon]
            },
        "properties": {
            # "Name":name,
            # "Date":dateTime,
            # "Movement":movement,
            # "minimumPressure":minimumPressure,
            # "maxSustainedWind":maxSustainedWind,
            },
    }

    #Append feature to feature list
    geojson['features'].append(feature)

    #Add fields to GeoJSON featre
    feature = {
        "type": "Feature",
         "geometry": {
            "type": "Point", "coordinates": [lon,lat]
            },
        "properties": {
            "Name":name,
            "Date":dateTime,
            "Movement":movement,
            "minimumPressure":minimumPressure,
            "maxSustainedWind":maxSustainedWind,
            },
    }

    #Append feature to feature list
    geojson['features'].append(feature)

#print(json.dumps(geojson, indent=4))

with open(output_file, "w") as file:
    json.dump(geojson, file, indent=4)
