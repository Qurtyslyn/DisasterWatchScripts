import json

zonesJSON = "./Zones.geojson"

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#Rename Name in Zones file to ID to match coastal (Which already has Name and ID)
for feature in zonesData['features']:
    if 'STATE_ZONE' in feature['properties'].keys():
        newZone = feature['properties']['STATE'] + 'Z' + feature['properties']['ZONE']
        feature['properties']['ID'] = newZone
    
with open(zonesJSON, 'w') as file:
    json.dump(zonesData, file)