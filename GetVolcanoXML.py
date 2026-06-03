import requests
import json
import re
import xml.etree.ElementTree as ET

#Setup Output file
output_file = "/var/www/DisasterWatch/Volcanoes.geojson"


#Get Data from Smithsonian source
url = "https://volcano.si.edu/news/WeeklyVolcanoCAP.xml"
response = requests.get(url)

response.raise_for_status()

#Setup XML Tree for parsing
xmlRoot = ET.fromstring(response.content)

#Remove Namespaces from tags
for element in xmlRoot.iter():
    if element.tag.startswith("{"):
        element.tag = element.tag.split("}",1)[1]

        for key in list(element.attrib.keys()):
            if key.startswith("{"):
                new_key = key.split("}",1)[1]
                element.attrib[new_key] = element.attrib.pop(key)

#Create GeoJSON variable to store relevant data in
geojson = {"type": "FeatureCollection", "features": []}

#Loop through XML and add to geojson Feature
for info in xmlRoot.findall("info"):
    
    #Get data from XML
    name = info.find("eventCode/value").text
    urgency = info.find("urgency").text
    severity = info.find("severity").text
    certainty = info.find("certainty").text
    description = info.find("description").text

    #Split up coordinates from string
    pointSplit = re.split(r"[, ]", info.find("area/circle").text)
    lat = pointSplit[0]
    lon = pointSplit[1]

    #Add fields to GeoJSON feature
    feature = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon,lat]},
        "properties": {"Urgency":urgency, 
                       "Severity":severity, 
                       "Certainty":certainty,
                       "Description":description,
                       "Name":name,
                       },
    }

    #Append feature to feature list
    geojson['features'].append(feature)

#Write file to WebServer for use
with open(output_file, "w") as file:
    json.dump(geojson, file, indent=4)
