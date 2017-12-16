import json

mods_data = open('./src/mods_parsed.json').read()
mods_json = json.loads(mods_data)
translations_data = open('./out/translations.json').read()
translations_json = json.loads(translations_data)

def getTranslation(id):
  for translation in translations_json:
    if (id in translation['ids']):
      return translation['descriptions'][0]['text']

keys = []

for mod in mods_json:
  for key in mod['spawnWeights'].keys():
    if ('shaper' in key or 'elder' in key):
      keys.append(key)

keys = sorted(set(keys))

mods = dict.fromkeys(keys)
for key in keys:
  mods[key] = []

for mod in mods_json:
  for key in mod['spawnWeights'].keys():
    if key in keys:
      if mod['spawnWeights'][key] > 0:
        mods[key].append(mod)

for key in keys:
  print(key)
  #print(' ')
  #for mod in mods[key]:
  #  for stat in mod['stats']:
  #    print(getTranslation(stat['id']))
  #print(' ')
  #print(' ')
  #print(' ')

