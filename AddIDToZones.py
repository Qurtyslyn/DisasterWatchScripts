import json

zonesJSON = "./NWSZones.geojson"

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#Rename Name in Zones file to ID to match coastal (Which already has Name and ID)
for feature in zonesData['features']:
    feature['properties']['ID'] = feature['properties']['STATE_ZONE']
    
with open(zonesJSON, 'w') as file:
    json.dump(zonesData, file)