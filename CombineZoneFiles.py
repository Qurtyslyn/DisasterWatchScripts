import json

#Main Zones File
zonesJSON = "./Zones.geojson"

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#New Zones Files
countyZones = './CountyZones.json'
fireZones = './FireZones.json'

# with open(countyZones, 'r') as file:
#     countyData = json.load(file)

# for feature in countyData['features']:
#     feature['properties']['ID'] = feature['properties']['STATE'] + 'C' + feature['properties']
#     print(feature['properties'])
#     break
print(len(zonesData['features']))

with open(fireZones, 'r') as file:
    fireData = json.load(file)

for feature in fireData['features']:
    feature['properties']['ID'] = feature['properties']['STATE'] + 'Z' + feature['properties']['ZONE']
    zonesData['features'].append(feature)

print(len(zonesData['features']))

with open(zonesJSON, 'w') as file:
    json.dump(zonesData, file)