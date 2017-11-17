import json
from collections import OrderedDict

class NPCMASTER:
  VORICI = 0
  TORA = 1
  CATARINA = 2
  ZANA = 3
  VAGAN = 4
  ELREON = 5
  HAKU = 6
  LEO = 7

# load json
craftingOptions_data = open('./src/CraftingBenchOptions.json').read()
craftingOptions_json = json.loads(craftingOptions_data)
itemClasses_data = open('./src/ItemClasses.json').read()
itemClasses_json = json.loads(itemClasses_data)
mods_data = open('./src/mods_parsed.json').read()
mods = json.loads(mods_data)
bases_data = open('./src/bases_parsed.json').read()
bases = json.loads(bases_data)
translations_data = open('./src/translations_parsed.json').read()
translations = json.loads(translations_data)

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

def transformValue(value, handler):
  if (handler == '60%_of_value'):
    return value * 0.6
  elif (handler == 'deciseconds_to_seconds'):
    return value * 10
  elif (handler == 'divide_by_one_hundred'):
    return value / 100
  elif (handler == 'divide_by_one_hundred_and_negate'):
    return -value / 100
  elif (handler == 'divide_by_one_hundred_2dp'):
    return '%.2f' % value / 100
  elif (handler == 'milliseconds_to_seconds'):
    return value / 1000
  elif (handler == 'milliseconds_to_seconds_0dp'):
    return '%.0f' % value / 1000
  elif (handler == 'milliseconds_to_Seconds_2dp'):
    return '%.2f' % value / 1000
  elif (handler == 'multiplicative_damage_modifier'):
    return value + 100
  elif (handler == 'multiplicative_permyriad_damage_modifier'):
    return value / 100 + 100
  elif (handler == 'negate'):
    return -value
  elif (handler == 'old_leech_percent'):
    return value / 5
  elif (handler == 'old_leech_permyriad'):
    return value / 500
  elif (handler == 'per_minute_to_per_second'):
    return '%.1f' % value / 60
  elif (handler == 'per_minute_to_per_second_0dp'):
    return '%.0f' % value / 60
  elif (handler == 'per_minute_to_per_second_2dp'):
    return '%.2f' % value / 60
  elif (handler == 'per_minute_to_per_second_2dp_if_required'):
    if (value / 60 % 1 == 0):
      return value / 60
    else:
      return '%.2f' % value / 60
  elif (handler == 'divide_by_ten_0dp'):
    return '%.0f' % value / 10
  elif (handler == 'divide_by_two_0dp'):
    return '%.0f' % value / 2
  elif (handler == 'divide_by_fifteen_0dp'):
    return '%.0f' % value / 15
  elif (handler == 'canonical_line'):
    return value
  else:
    return value

def getItemTypes(keys):
  out = []
  for key in keys:
    out.append(itemClasses[key]['Id'])
  return out

def getCustomAction(remove, sockets, colors, links):
  removeMod = False
  if (remove == 1):
    removeMod = True
  socketsValue = None
  if (sockets > 0):
    socketsValue = sockets
  colorsValue = None
  if (len(colors) > 0):
    colorsValue = colors
  linksValue = None
  if (links > 0):
    linksValue = links
  return OrderedDict([
    ('removeMod', removeMod),
    ('sockets', socketsValue),
    ('colors', colorsValue),
    ('links', linksValue)
  ])

def getDesc(translation, values):
  for desc in translation['descriptions']:
    for condition in desc['conditions']:
      for value in values:
        if ((condition['min'] == None or value['valueMin'] >= condition['min']) and 
        (condition['max'] == None or value['valueMax'] <= condition['max'])):
          return desc;    

def getText(option):
  disabled = [
    'dummy_stat_display_nothing',
  ]
  summoner = [
    'base_number_of_skeletons_allowed',
    'base_number_of_zombies_allowed',
    'base_number_of_spectres_allowed'
  ]
  if (option['ModsKey'] != None):
    mod = mods[option['ModsKey']]
    ids = [x['id'] for x in mod['stats'] if x['id'] not in disabled]
    translation = [x for x in translations if x['ids'] == ids]

    if (len(translation) > 0):
      translation = translation[0]
      values = []
      for stat in mod['stats']:
        values.append({
          'id': stat['id'], 
          'valueMin': stat['valueMin'], 
          'valueMax': stat['valueMax']
        })
      match = getDesc(translation, values)
      valueRanges = []
      for value in values:
        handler = ''
        try:
          handler = match['indexHandlers'][values.index(value)]
        except IndexError:
          handler = ''
        valueMin = transformValue(value['valueMin'], handler)
        valueMax = transformValue(value['valueMax'], handler)
        valueRange = ''
        if (valueMin == valueMax):
          valueRange = str(valueMax)
        else:
          valueRange = '(' + str(valueMin) + '-' + str(valueMax) + ')'
        format = ''
        try:
          format = match['formats'][values.index(value)]
        except IndexError:
          format = ''
        if ('%' in format):
          valueRange += '%'
        valueRanges.append(valueRange)
      return [match['text'].format(*valueRanges)]
    else:
      out = []
      for statId in ids:
        values = []
        for stat in mod['stats']:
          if (stat['id'] == statId):
            values.append({
              'id': stat['id'], 
              'valueMin': stat['valueMin'], 
              'valueMax': stat['valueMax']
            })
        translation = [x for x in translations if statId in x['ids']][0]
        match = getDesc(translation, values)
        valueRanges = []
        for value in values:
          handler = ''
          try:
            handler = match['indexHandlers'][values.index(value)]
          except IndexError:
            handler = ''
          valueMin = transformValue(value['valueMin'], handler)
          valueMax = transformValue(value['valueMax'], handler)
          valueRange = ''
          if (valueMin == valueMax):
            valueRange = str(valueMax)
          else:
            valueRange = '(' + str(valueMin) + '-' + str(valueMax) + ')'
          format = ''
          try:
            format = match['formats'][values.index(value)]
          except IndexError:
            format = ''
          if ('(' not in valueRange and '+' in format):
            valueRange = '+' + valueRange
          if ('%' in format):
            valueRange += '%'
          valueRanges.append(valueRange)
        if (statId not in summoner or '0' not in valueRanges[0]):
          out.append(match['text'].format(*valueRanges))
      return out
  return None

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
  if (not option['IsDisabled'] and not option['NPCMasterKey'] == NPCMASTER.ZANA):
    out = OrderedDict([
      ('name', name),
      ('text', getText(option)),
      ('order', option['Order']),
      ('mod', mod),
      ('costItem', bases[option['Cost_BaseItemTypesKeys'][0]]['name']),
      ('costValue', option['Cost_Values'][0]),
      ('master', option['NPCMasterKey']),
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
