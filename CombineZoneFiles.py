import json

#Main Zones File
zonesJSON = "./Zones.geojson"

with open(zonesJSON, 'r') as file:
    zonesData = json.load(file)

#New Zones Files
countyZones = './CountyZones.json'
fireZones = './FireZones.json'
countyIDs = 'CountyZoneIDs.json'
oceanZones = './OceanZones.json'
seaZones = './SeaZones.json'


# with open(countyZones, 'r') as file:
#     countyData = json.load(file)

# with open(oceanZones, 'r') as file:
#     oceanData = json.load(file)

with open(seaZones, 'r') as file:
    seaData = json.load(file)

# with open(countyIDs, 'r') as file:
#     countyIDData = json.load(file)

for feature in seaData['features']:
    zonesData['features'].append(feature)


#print(len(zonesData['features']))
# for feature in countyData['features']:
#     #feature['properties']['ID'] = feature['properties']['STATE'] + 'C' + feature['properties']
    

#     data = next((item for item in countyIDData['features'] if (item['properties']['name'] == feature['properties']['COUNTYNAME'] and item['properties']['state'] == feature['properties']['STATE'] )), None)
    
#     if data == None:
#         continue

#     feature['properties']['ID'] = data['properties']['id']
    

#     zonesData['features'].append(feature)

#print(len(zonesData['features']))

# with open(fireZones, 'r') as file:
#     fireData = json.load(file)

# for feature in fireData['features']:
#     feature['properties']['ID'] = feature['properties']['STATE'] + 'Z' + feature['properties']['ZONE']
#     zonesData['features'].append(feature)

# print(len(zonesData['features']))

with open(zonesJSON, 'w') as file:
    json.dump(zonesData, file)