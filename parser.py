import json

mods_data = open('./src/Mods.json').read()
mods_json = json.loads(mods_data)

headers = []
for header in mods_json[0]['header']:
  headers.append(header['name'])

mods = []
for mod in mods_json[0]['data']:
  mods.append(dict(zip(headers, mod)))

print(mods[0])