import re
import json

statIds = re.compile('(\d)+ (.*)')
descriptions = []

with open('./src/stat_descriptions.txt', encoding='utf-16') as f:
  for line in f:
    if line.strip().startswith('description'):
      m = statIds.match(f.readline().strip())
      idCount = int(m.group(1))
      ids = m.group(2).split(' ')
      n = int(f.readline().strip())
      rawDescriptions = []
      for i in range(n):
        rawDescriptions.append(f.readline().strip())
      statDescription = dict([
        ('ids', ids),
        ('idCount', idCount),
        ('descriptions', rawDescriptions)
      ])
      descriptions.append(statDescription)

with open('./out/descriptions.json', 'w+') as out:
  json.dump(descriptions, out)