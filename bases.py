import json
import re
from collections import OrderedDict

# load json
baseItemTypes_data = open('./src/BaseItemTypes.json').read()
baseItemTypes_json = json.loads(baseItemTypes_data)
tags_data = open('./src/Tags.json').read()
tags_json = json.loads(tags_data)
itemClasses_data = open('./src/ItemClasses.json').read()
itemClasses_json = json.loads(itemClasses_data)
itemVisualIdentity_data = open('./src/ItemVisualIdentity.json').read()
itemVisualIdentity_json = json.loads(itemVisualIdentity_data)
shieldTypes_data = open('./src/ShieldTypes.json').read()
shieldTypes_json = json.loads(shieldTypes_data)
weaponTypes_data = open('./src/WeaponTypes.json').read()
weaponTypes_json = json.loads(weaponTypes_data)
componentArmour_data = open('./src/ComponentArmour.json').read()
componentArmour_json = json.loads(componentArmour_data)
componentAttributeRequirements_data = open('./src/ComponentAttributeRequirements.json').read()
componentAttributeRequirements_json = json.loads(componentAttributeRequirements_data)
mods_data = open('./src/mods_parsed.json').read()
mods = json.loads(mods_data)

# bases
bases_headers = []
for header in baseItemTypes_json[0]['header']:
  bases_headers.append(header['name'])

bases = []
for base in baseItemTypes_json[0]['data']:
  bases.append(dict(zip(bases_headers, base)))

# tags
tags = []
for tag in tags_json[0]['data']:
  tags.append(tag[0])

# item classes
itemClasses_headers = []
for header in itemClasses_json[0]['header']:
  itemClasses_headers.append(header['name'])

itemClasses = []
for itemClass in itemClasses_json[0]['data']:
  itemClasses.append(dict(zip(itemClasses_headers, itemClass)))

# item visual identity
artPaths = []
for art in itemVisualIdentity_json[0]['data']:
  artPaths.append(art[1])

# shield types
shieldTypes_headers = []
for header in shieldTypes_json[0]['header']:
  shieldTypes_headers.append(header['name'])

shieldTypes = []
for shieldType in shieldTypes_json[0]['data']:
  shieldTypes.append(dict(zip(shieldTypes_headers, shieldType)))

# weapon types
weaponTypes_headers = []
for header in weaponTypes_json[0]['header']:
  weaponTypes_headers.append(header['name'])

weaponTypes = []
for weaponType in weaponTypes_json[0]['data']:
  weaponTypes.append(dict(zip(weaponTypes_headers, weaponType)))

# component armour
componentArmour_headers = []
for header in componentArmour_json[0]['header']:
  componentArmour_headers.append(header['name'])

defenses = []
for defense in componentArmour_json[0]['data']:
  defenses.append(dict(zip(componentArmour_headers, defense)))

# component attribute requirements
componentAttributeRequirements_headers = []
for header in componentAttributeRequirements_json[0]['header']:
  componentAttributeRequirements_headers.append(header['name'])

requirements = []
for requirement in componentAttributeRequirements_json[0]['data']:
  requirements.append(dict(zip(componentAttributeRequirements_headers, requirement)))

### implicits that are hidden
# talisman can be picked up
hiddenImplicits = [6972]
# flask level requirements
for i in range(2925, 2948):
  hiddenImplicits.append(i)
# movement penatlies
for i in range(3170, 3174):
  hiddenImplicits.append(i)

def parseOTFile(path):
  output = dict([
    ('parentTags', None),
    ('sockets', None)
  ])
  parentTags = []
  sockets = 0
  while True:
    f = open('./src/' + path + '.ot', encoding='utf-16').readlines()
    parentLine = [x for x in f if 'extends' in x][0].strip()
    path = re.match('extends "(.*)"', parentLine).group(1)
    tagLines = [x for x in f if ('tag = ' in x and 'remove_tag' not in x)]
    for tagLine in tagLines:
      tag = re.match('tag = "(.*)"', tagLine.strip()).group(1)
      parentTags.append(tag)
    socketLine = [x for x in f if 'socket_info' in x]
    if (len(socketLine) > 0 and sockets == 0):
      socketMatch = re.match('socket_info = "\d+:(\d+):\d+ \d+:(\d+):\d+ \d+:(\d+):\d+ \d+:(\d+):\d+ \d+:(\d+):\d+ \d+:(\d+):\d+"', socketLine[0].strip())
      for i in range(1, 7):
        if (int(socketMatch.group(i)) < 9999):
          sockets += 1        
    if path == 'nothing':
      break
  output['parentTags'] = parentTags
  output['sockets'] = sockets
  return output


def parseBase(base):
  # to be used later
  OTFile = parseOTFile(base['InheritsFrom'])

  baseId = base['Id']
  name = base['Name']

  baseType = itemClasses[base['ItemClassesKey']]['Id']
  if (' Hand ' in baseType):
    baseType = re.sub(' Hand ', ' Handed ', baseType)

  category = itemClasses[base['ItemClassesKey']]['Category']
  if (category == ''):
    if (baseType == 'FishingRod'):
      category = 'Fishing Rod'
    elif (baseType == 'UtilityFlaskCritical'):
      category = 'Flasks'

  dropLevel = base['DropLevel']

  ### implicit
  implicit = None
  # should have max 2 keys, if 2 keys 1 is always hidden
  for key in base['Implicit_ModsKeys']:
    if (key not in hiddenImplicits):
      implicit = mods[key]
  
  ### tags
  baseTags = []
  for key in base['TagsKeys']:
    baseTags.append(tags[key])
  baseTags += OTFile['parentTags']
  # remove duplicate tags (sceptre)
  def distinct(list):
    seen = set()
    return [x for x in list if x not in seen and not seen.add(x)]
  baseTags = distinct(baseTags)
  
  ### requirement
  requirement = None
  componentRequirement = [x for x in requirements if x['BaseItemTypesKey'] == base['Id']]
  if (len(componentRequirement) > 0):
    requirement = dict([
      ('level', base['DropLevel']),
      ('str', componentRequirement[0]['ReqStr']),
      ('dex', componentRequirement[0]['ReqDex']),
      ('int', componentRequirement[0]['ReqInt'])
    ])
  else:
    requirement = dict([
      ('level', base['DropLevel']),
      ('str', 0),
      ('dex', 0),
      ('int', 0)
    ])

  ### defense
  defense = None
  componentArmour = [x for x in defenses if x['BaseItemTypesKey'] == base['Id']]
  if (len(componentArmour) > 0):
    defense = dict([
      ('armor', componentArmour[0]['Armour']),
      ('evasion', componentArmour[0]['Evasion']),
      ('energyShield', componentArmour[0]['EnergyShield']),
      # to be filled later
      ('block', None)
    ])

  ### weapon
  # to be filled later
  weapon = None

  ### sockets
  maxSockets = OTFile['sockets']
  verticalSockets = True if (maxSockets > 1 and base['Width'] == 1) else False

  ### art
  ddsPath = artPaths[base['ItemVisualIdentityKey']]
  artPath = 'web.poecdn.com/image/' + ddsPath.replace('.dds', '.png')

  return dict([
    ('id', baseId),
    ('name', name),
    ('type', baseType),
    ('category', category),
    ('dropLevel', dropLevel),
    ('implicit', implicit),
    ('tags', baseTags),
    ('artPath', artPath),
    ('maxSockets', maxSockets),
    ('verticalSockets', verticalSockets),
    ('requirement', requirement),
    ('defense', defense),
    ('weapon', weapon)
  ])

parsedBases = []
for base in bases:
  parsedBases.append(parseBase(base))

### add block
for shield in shieldTypes:
  parsedBases[shield['BaseItemTypesKey']]['defense']['block'] = shield['Block']

### add weapon
def getWeapon(weapon):
  return dict([
    ('damageMin', weapon['DamageMin']),
    ('damageMax', weapon['DamageMax']),
    ('crit', weapon['Critical']),
    ('speed', weapon['Speed']),
    ('range', weapon['RangeMax'])
  ])
for weapon in weaponTypes:
  parsedBases[weapon['BaseItemTypesKey']]['weapon'] = getWeapon(weapon)


with open('./src/bases_parsed.json', 'w+') as out:
  json.dump(parsedBases, out)

###
ids = [
  'Metadata/Items/Amulet',
  'Metadata/Items/Amulets',
  'Metadata/Items/Armours',
  'Metadata/Items/Belts',
  'Metadata/Items/Jewels',
  'Metadata/Items/Quivers',
  'Metadata/Items/Rings',
  'Metadata/Items/Weapons',
  'Metadata/Items/Amulet',
]
parsedBases = [x for x in parsedBases if (any(itemID in x['id'] for itemID in ids) and 'Talismans' not in x['id'] and 'Keyblade' not in x['name'] and 'Fishing Rod' not in x['category'] and 'Kaom\'s' not in x['name'])]
###

with open('./out/bases.json', 'w+') as out:
  json.dump(parsedBases, out)