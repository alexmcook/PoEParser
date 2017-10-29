import re
import json
from collections import OrderedDict

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
  matches = re.findall('%\d([\$\+d%]*)%|%\d(\$\+?d)', textRaw)
  for match in matches:
    if ((match[0] == '' and match[1] == '') or match[1] == '$d'):
      formats.append('#')
    elif (match[0] == '%%' or match[0] == '$d%'):
      formats.append('#%')
    elif (match[1] == '$+d'):
      formats.append('+#')
    elif (match[0] == '$+d%'):
      formats.append('+#%')
    else:
      raise Exception('No format found for ' + textRaw)
  ### replace ex %1$+d%% with {0}
  def repl(match):
    return '{' + str(int(match.group(1)) - 1) + '}'
  text = re.sub('%(\d)([\w\d\+\$%]*%|\$\+?d)', repl, textRaw)
  ### replace %% with %
  text = re.sub('([^%])(%%)([^%])', '\\1%\\3', text)
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

descriptions = []
with open('./src/stat_descriptions.txt', encoding='utf-16') as f:
  for line in f:
    if line.strip().startswith('description'):
      m = re.match('(\d)+ (.*)', f.readline().strip())
      idCount = int(m.group(1))
      ids = m.group(2).split(' ')
      n = int(f.readline().strip())
      rawDescriptions = []
      for i in range(n):
        rawDescriptions.append(f.readline().strip())
      parsedDescriptions = []
      for raw in rawDescriptions:
        parsedDescriptions.append(parseDescription(raw))
      statDescription = OrderedDict([
        ('ids', ids),
        #('idCount', idCount),
        ('descriptions', parsedDescriptions)
      ])
      descriptions.append(statDescription)

with open('./out/descriptions.json', 'w+') as out:
  json.dump(descriptions, out)