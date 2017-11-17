import json
from collections import OrderedDict

class NPCMASTER:
  VORICI = 1,
  TORA = 2,
  CATARINA = 3,
  ZANA = 4,
  VAGAN = 5,
  ELREON = 6,
  HAKU = 7,
  LEO = 8

# load json
craftingOptions_data = open('./src/CraftingBenchOptions.json').read()
craftingOptions_json = json.loads(craftingOptions_data)
itemClasses_data = open('./src/ItemClasses.json').read()
itemClasses_json = json.loads(itemClasses_data)
mods_data = open('./src/mods_parsed.json').read()
mods = json.loads(mods_data)
bases_data = open('./src/bases_parsed.json').read()
bases = json.loads(bases_data)

# craftingOptions
craftingOptions_headers = []
for header in craftingOptions_json[0]['header']:
  craftingOptions_headers.append(header['name'])

craftingOptions = []
for craftingOption in craftingOptions_json[0]['data']:
  craftingOptions.append(dict(zip(craftingOptions_headers, craftingOption)))

# item classes
itemClasses_headers = []
for header in itemClasses_json[0]['header']:
  itemClasses_headers.append(header['name'])

itemClasses = []
for itemClass in itemClasses_json[0]['data']:
  itemClasses.append(dict(zip(itemClasses_headers, itemClass)))

def getItemTypes(keys):
  out = []
  for key in keys:
    out.append(itemClasses[key]['Id'])
  return out

def getCustomAction(remove, sockets, colors, links):
  removeMod = False
  if (remove == 1):
    removeMod = True
  return OrderedDict([
    ('removeMod', removeMod),
    ('sockets', sockets),
    ('colors', colors),
    ('links', links)
  ])

def parseCraftingOption(option):
  if (option['ModsKey'] != None):
    mod = mods[option['ModsKey']]
    for stat in mod['stats']:
      if (stat['key'] and stat['key'] < 10000):
        stat['key'] += 10000
    name = mod['id']
  else:
    mod = None
    name = option['Name']
  if (not option['IsDisabled']):
    out = OrderedDict([
      ('name', name),
      ('order', option['Order']),
      ('mod', mod),
      ('costItem', bases[option['Cost_BaseItemTypesKeys'][0]]['name']),
      ('costValue', option['Cost_Values'][0]),
      ('masterLevel', option['MasterLevel']),
      ('itemTypes', getItemTypes(option['ItemClassesKeys'])),
      ('customAction', getCustomAction(
        option['CraftingBenchCustomAction'],
        option['Sockets'],
        option['SocketColours'],
        option['Links']
      ))
    ])
    return out

parsedCraftingOptions = []
for craftingOption in craftingOptions:
  parsed = parseCraftingOption(craftingOption)
  if (parsed):
    parsedCraftingOptions.append(parseCraftingOption(craftingOption))

with open('./out/craftingOptions.json', 'w+') as out:
  json.dump(parsedCraftingOptions, out)
