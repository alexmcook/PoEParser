import json
from collections import OrderedDict

# load json
essences_data = open('./src/Essences.json').read()
essences_json = json.loads(essences_data)
essenceType_data = open('./src/EssenceType.json').read()
essenceType_json = json.loads(essenceType_data)
baseItemTypes_data = open('./src/BaseItemTypes.json').read()
baseItemTypes_json = json.loads(baseItemTypes_data)
mods_data = open('./src/mods_parsed.json').read()
mods = json.loads(mods_data)

# essences
essences_headers = []
for header in essences_json[0]['header']:
  essences_headers.append(header['name'])

essences = []
for essence in essences_json[0]['data']:
  essences.append(OrderedDict(zip(essences_headers, essence)))

# essenceType
essenceType_headers = []
for header in essenceType_json[0]['header']:
  essenceType_headers.append(header['name'])

essenceTypes = []
for essenceType in essenceType_json[0]['data']:
  essenceTypes.append(OrderedDict(zip(essenceType_headers, essenceType)))

# bases
bases_headers = []
for header in baseItemTypes_json[0]['header']:
  bases_headers.append(header['name'])

bases = []
for base in baseItemTypes_json[0]['data']:
  bases.append(dict(zip(bases_headers, base)))

def parseEssence(essence):
  essenceId = bases[essence['BaseItemTypesKey']]['Id']
  minTier = essenceTypes[essence['EssenceTypeKey']]['EssenceType']
  if minTier == 6:
    minTier = 8
  if (essenceId != 'Metadata/Items/Currency/CurrencyCorruptMonolith'):
    out = OrderedDict([
      ('id', essenceId),
      ('minTier', minTier),
      ('name', essenceTypes[essence['EssenceTypeKey']]['Id']),
      ('amulet', mods[essence['Amulet2_ModsKey']]),
      ('belt', mods[essence['Belt2_ModsKey']]),
      ('ring', mods[essence['Ring_ModsKey']]),
      ('quiver', mods[essence['Quiver_ModsKey']]),
      ('body', mods[essence['BodyArmour2_ModsKey']]),
      ('boots', mods[essence['Boots2_ModsKey']]),
      ('gloves', mods[essence['Gloves2_ModsKey']]),
      ('helmet', mods[essence['Helmet2_ModsKey']]),
      ('shield', mods[essence['Shield2_ModsKey']]),
      ('oneHand', mods[essence['1Hand_ModsKey2']]),
      ('twoHand', mods[essence['2Hand_ModsKey2']]),
      ('bow', mods[essence['Bow_ModsKey']]),
      ('wand', mods[essence['Wand_ModsKey']])
    ])
    return out

parsedEssences = []
for essence in essences:
  parsed = parseEssence(essence)
  if (parsed):
    parsedEssences.append(parsed)

with open('./out/essences.json', 'w+') as out:
  json.dump(parsedEssences, out, ensure_ascii=False)
