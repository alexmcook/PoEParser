import re
import json
from collections import OrderedDict


mod_ids_data = open('./src/mod_ids_parsed.json').read()
mod_ids = json.loads(mod_ids_data)

def parseDescription(desc):
  conditions = []
  conditions = []
  text = None
  formats = []
  indexHandlers=[]

  parts = desc.split('"')
  # parts[0] -> conditions
  conditionsLine = parts[0].strip().split()
  for condition in conditionsLine:
    conditionMin = None
    conditionMax = None
    if '|' in condition.strip():
      conditionValues = condition.strip().split('|')
      if (conditionValues[0] != '#'):
        conditionMin = int(conditionValues[0])
      if (conditionValues[1] != '#'):
        conditionMax = int(conditionValues[1])
    else:
      if (condition.strip() != '#'):
        conditionMin = int(condition.strip())
        conditionMax = int(condition.strip())
    conditions.append(OrderedDict([
      ('min', conditionMin),
      ('max', conditionMax)
    ]))
  # parts[1] -> string
  textRaw = parts[1].strip()
  matches = re.findall('%[\dd]([\$\+d%]*)%|%\d(\$\+?d)', textRaw)
  for match in matches:
    if ((match[0] == '' and match[1] == '') or match[1] == '$d'):
      formats.append('#')
    elif (match[0] == '%' or match[0] == '%%' or match[0] == '$d%'):
      formats.append('#%')
    elif (match[1] == '$+d'):
      formats.append('+#')
    elif (match[0] == '$+d%'):
      formats.append('+#%')
    else:
      raise Exception('No format found for ' + textRaw)
  ### replace ex %1$+d%% with {0}
  def repl(match):
    m = match.group(1)
    if (m == 'd'):
      m = '0'
    else:
      m = str(int(m) - 1)
    return '{' + m + '}'
  text = re.sub('%([\dd])([\w\d\+\$%]*%|\$\+?d)', repl, textRaw)
  ### replace %% with %
  text = re.sub('([^%d])(%%)([^%])', '\\1%\\3', text)
  # parts[2] -> indexHandlers/reminders
  indexHandlerLine = parts[2].strip().split()
  for element in indexHandlerLine:
    if (element in '0123456789' or 'reminder' in element.lower() or element == ''):
      break
    indexHandlers.append(element)

  return OrderedDict([
    ('conditions', conditions),
    ('text', text),
    ('formats', formats),
    ('indexHandlers', indexHandlers)
  ])

translations = []
with open('./src/stat_descriptions.txt', encoding='utf-16') as f:
  for line in f:
    if line.strip().startswith('description'):
      m = re.match('(\d)+ (.*)', f.readline().strip())
      idCount = int(m.group(1))
      ids = m.group(2).split()
      n = int(f.readline().strip())
      rawDescriptions = []
      for i in range(n):
        rawDescriptions.append(f.readline().strip())
      parsedDescriptions = []
      ### Fix for base_chance_to_freeze_% including a second unused id
      if 'always_freeze' in ids:
        for raw in rawDescriptions:
          parsedDescriptions.append(parseDescription(raw))
        for desc in parsedDescriptions:
          desc['conditions'] = [desc['conditions'][0]]
          desc['indexHandlers'] = []
        statDescription = OrderedDict([
          ('ids', ids[0:1]),
          #('idCount', idCount),
          ('descriptions', parsedDescriptions[1:])
        ])
        translations.append(statDescription)
      else :
        for raw in rawDescriptions:
          parsedDescriptions.append(parseDescription(raw))
        statDescription = OrderedDict([
          ('ids', ids),
          #('idCount', idCount),
          ('descriptions', parsedDescriptions)
        ])
        translations.append(statDescription)

with open('./src/translations_parsed.json', 'w+') as out:
  json.dump(translations, out, ensure_ascii=False)

###
translations = [x for x in translations if (any(mod_id in x['ids'] for mod_id in mod_ids))]
###

with open('./out/translations.json', 'w+') as out:
  json.dump(translations, out, ensure_ascii=False)