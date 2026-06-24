import json

#Setup Output file
output_file = "./ZonesCD.geojson"

#GeoJSON Files
coastalJSON = "./NWSCoastalZones.geojson"
zonesJSON = "./NWSZones.geojson"

#Load local GeoJSON files
with open(coastalJSON, 'r') as file:
    coastalData = json.load(file)

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

for feature in coastalData['features']:
    feature['properties'].pop("WFO", None)
    feature['properties'].pop("GL_WFO", None)
    feature['properties'].pop("NAME", None)
    feature['properties'].pop("LON", None)
    feature['properties'].pop("LAT", None)

for feature in zonesData['features']:
    feature['properties'].pop("STATE", None)
    feature['properties'].pop("CWA", None)
    feature['properties'].pop("TIME_ZONE", None)
    feature['properties'].pop("FE_AREA", None)
    feature['properties'].pop("ZONE", None)
    feature['properties'].pop("STATE_ZONE", None)
    feature['properties'].pop("LON", None)
    feature['properties'].pop("LAT", None)
    feature['properties'].pop("SHORTNAME", None)


#Combine Zones
coastalData['features'] = coastalData['features'] + zonesData['features']

zones = coastalData

with open(output_file, 'w') as file:
    json.dump(zones, file, separators=(',',':'), ensure_ascii=False)