import requests
import xml.etree.ElementTree as ET

#Download initial KML File and parse to get each Hurricane
url = "https://www.nhc.noaa.gov/gis/kml/nhc_active.kml"
response = requests.get(url)

response.raise_for_status()

#Setup XML Tree for parsing
kmlRoot = ET.fromstring(response.content)

#Create GeoJSON variable to store relevant data in
geojson = {"type": "FeatureCollection", "features": []}

#For each hurricane, get the Data and download the follwing
#KMZ files to be unzipped
#Best Track
#Cone of Uncertainty
#Predicted Track
#Extent of Winds
for folder in kmlRoot.findall("Folder"):
    if folder.get('id') == "wsp":
        continue

    #Get data from KML
    name = folder.find("tcName").text
    lat = folder.find("centerLat").text
    lon = folder.find("centerLon").text
    dateTime = folder.find("dateTime").text
    movement = folder.find("movement").text
    minimumPressure = folder.find("minimumPressure").text
    maxSustainedWind = folder.find("maxSustainedWind").text

    #Add fields to GeoJSON featre

    feature = {
        "type": "Feature",
         "geometry": {"type": "Point", "coordinates": [lon,lat]},
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

