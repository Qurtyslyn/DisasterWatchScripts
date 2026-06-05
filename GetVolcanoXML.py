import requests
from bs4 import BeautifulSoup as BS
import json
import re
import xml.etree.ElementTree as ET

#Setup Output file
output_file = "/var/www/DisasterWatch/Volcanoes.geojson"

#Headers for web requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

#Get Data from Smithsonian source
url = "https://volcano.si.edu/news/WeeklyVolcanoCAP.xml"
response = requests.get(url, headers=headers)

response.raise_for_status()

#Get Data from Smithsonian Web Page
url = "https://volcano.si.edu/reports_weekly.cfm"
webpage = requests.get(url, headers=headers)

webpage.raise_for_status()

#Parse Website table for additional Volcano info
pageData = BS(webpage.content, "html.parser")

table = pageData.find("tbody")
tableData = {}

#Loop Through Table rows and add data to tableData
for row in table.find_all("tr"):
    cells = row.find_all("td")
    
    #Strip the HTML from the cells
    cells = [element.text.strip() for element in cells]

    if cells:
        tableData[cells[0]] = {"Country":cells[1],"Region":cells[2],"Date":cells[3],"ReportType":cells[4]}

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
                       "StartDate":tableData[name]["Date"],
                       "Country":tableData[name]["Country"],
                       "Region":tableData[name]["Region"],
                       "ReportType":tableData[name]["ReportType"],
                       },
    }

    #Append feature to feature list
    geojson['features'].append(feature)

#Write file to WebServer for use
with open(output_file, "w") as file:
    json.dump(geojson, file, indent=4)
