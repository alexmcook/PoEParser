import json
from collections import OrderedDict

class DOMAIN:
  ITEM = 1
  FLASK = 2
  MONSTER = 3
  CHEST = 4
  AREA = 5
  UNKNOWN1 = 6
  UNKNOWN2 = 7
  UNKNOWN3 = 8
  STANCE = 9
  MASTER = 10
  JEWEL = 11
  ATLAS = 12
  LEAGUESTONE = 13

class GENERATION_TYPE:
  PREFIX = 1
  SUFFIX = 2
  UNIQUE = 3
  NEMESIS = 4
  CORRUPTED = 5
  BLOODLINES = 6
  TORMENT = 7
  TEMPEST = 8
  TALISMAN = 9
  ENCHANTMENT = 10
  ESSENCE = 11

# load json
mods_data = open('./src/Mods.json').read()
mods_json = json.loads(mods_data)
modType_data = open('./src/ModType.json').read()
modType_json = json.loads(modType_data)
tags_data = open('./src/Tags.json').read()
tags_json = json.loads(tags_data)
stats_data = open('./src/Stats.json').read()
stats_json = json.loads(stats_data)
translations_data = open('./out/translations.json').read()
translations_json = json.loads(translations_data)

# mods
mods_headers = []
for header in mods_json[0]['header']:
  mods_headers.append(header['name'])

mods = []
for mod in mods_json[0]['data']:
  mods.append(OrderedDict(zip(mods_headers, mod)))

# stats
stats_headers = []
for header in stats_json[0]['header']:
  stats_headers.append(header['name'])

stats = []
for stat in stats_json[0]['data']:
  stats.append(OrderedDict(zip(stats_headers, stat)))

# modType
modTypes = []
for modType in modType_json[0]['data']:
  modTypes.append(modType[0])

# tags
tags = []
for tag in tags_json[0]['data']:
  tags.append(tag[0])

def getStats(mod):
  mod_stats = []
  if (mod['StatsKey1'] != None):
    key = None
    for i, desc in enumerate(translations_json):
      if stats[mod['StatsKey1']]['Id'] in desc['ids']:
        key = i
        if ('Master' in mod['Id'] and 'Vendor' not in mod['Id']):
          key += 10000
    stat1 = OrderedDict([
      ('id', stats[mod['StatsKey1']]['Id']),
      ('valueMin', mod['Stat1Min']),
      ('valueMax', mod['Stat1Max']),
      ('value', None),
      ('key', key)])
    mod_stats.append(stat1)
  if (mod['StatsKey2'] != None):
    key = None
    for i, desc in enumerate(translations_json):
      if stats[mod['StatsKey2']]['Id'] in desc['ids']:
        key = i
        if ('Master' in mod['Id'] and 'Vendor' not in mod['Id']):
          key += 10000
    stat2 = OrderedDict([
      ('id', stats[mod['StatsKey2']]['Id']),
      ('valueMin', mod['Stat2Min']),
      ('valueMax', mod['Stat2Max']),
      ('value', None),
      ('key', key)])
    mod_stats.append(stat2)
  if (mod['StatsKey3'] != None):
    key = None
    for i, desc in enumerate(translations_json):
      if stats[mod['StatsKey3']]['Id'] in desc['ids']:
        key = i
        if ('Master' in mod['Id'] and 'Vendor' not in mod['Id']):
          key += 10000
    stat3 = OrderedDict([
      ('id', stats[mod['StatsKey3']]['Id']),
      ('valueMin', mod['Stat3Min']),
      ('valueMax', mod['Stat3Max']),
      ('value', None),
      ('key', key)])
    mod_stats.append(stat3)
  if (mod['StatsKey4'] != None):
    key = None
    for i, desc in enumerate(translations_json):
      if stats[mod['StatsKey4']]['Id'] in desc['ids']:
        key = i
        if ('Master' in mod['Id'] and 'Vendor' not in mod['Id']):
          key += 10000
    stat4 = OrderedDict([
      ('id', stats[mod['StatsKey4']]['Id']),
      ('valueMin', mod['Stat4Min']),
      ('valueMax', mod['Stat4Max']),
      ('value', None),
      ('key', key)])
    mod_stats.append(stat4)
  if (mod['StatsKey5'] != None):
    key = None
    for i, desc in enumerate(translations_json):
      if stats[mod['StatsKey5']]['Id'] in desc['ids']:
        key = i
        if ('Master' in mod['Id'] and 'Vendor' not in mod['Id']):
          key += 10000
    stat5 = OrderedDict([
      ('id', stats[mod['StatsKey5']]['Id']),
      ('valueMin', mod['Stat5Min']),
      ('valueMax', mod['Stat5Max']),
      ('value', None),
      ('key', key)])
    mod_stats.append(stat5)
  return mod_stats

def getSpawnWeights(mod):
  spawnWeightTags = []
  for key in mod['SpawnWeight_TagsKeys']:
    spawnWeightTags.append(tags[key])
  return OrderedDict(zip(spawnWeightTags, mod['SpawnWeight_Values']))

def getGenerationWeights(mod):
  generationWeightTags = []
  for key in mod['GenerationWeight_TagsKeys']:
    generationWeightTags.append(tags[key])
  return OrderedDict(zip(generationWeightTags, mod['GenerationWeight_Values']))

def getTags(mod):
  modTags = []
  for key in mod['TagsKeys']:
    modTags.append(tags[key])
  return modTags

def parseMod(mod):
  out = OrderedDict([
    ('id', mod['Id']),
    ('name', mod['Name']),
    ('modType', modTypes[mod['ModTypeKey']]),
    ('group', mod['CorrectGroup']),
    ('level', mod['Level']),
    ('domain', mod['Domain']),
    ('generationType', mod['GenerationType']),
    ('tags', getTags(mod)),
    ('stats', getStats(mod)),
    ('spawnWeights', getSpawnWeights(mod)),
    ('generationWeights', getGenerationWeights(mod)),
    ('essenceOnly', mod['IsEssenceOnlyModifier']),
  ])
  return out

parsedMods = []
for mod in mods:
  parsedMods.append(parseMod(mod))

with open('./src/mods_parsed.json', 'w+') as out:
  json.dump(parsedMods, out, ensure_ascii=False)

###
domains = [DOMAIN.ITEM, DOMAIN.JEWEL, DOMAIN.MASTER]
parsedMods = [x for x in parsedMods if x['domain'] in domains]
###

with open('./out/mods.json', 'w+') as out:
  json.dump(parsedMods, out, ensure_ascii=False)