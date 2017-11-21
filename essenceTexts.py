import os.path
import re
import json
import requests
from collections import OrderedDict

tier = [
  '',
  'Whispering',
  'Muttering',
  'Weeping',
  'Wailing',
  'Screaming',
  'Shrieking',
  'Deafening',
  ''
]

# load json
essences_data = open('./src/essences_parsed.json').read()
essences = json.loads(essences_data)

data = []

if (not os.path.exists('./src/essence_data.json')):
  for essence in essences:
    url = 'https://pathofexile.gamepedia.com/api.php?action=browsebysubject&format=json&subject='
    if (tier[essence['tier']] != ''):
      url += tier[essence['tier']] + '%20'
    url += 'Essence%20of%20' + essence['name']
    r = requests.get(url)
    if (r.status_code == 200):
      essenceID = ' '
      if (tier[essence['tier']] != ''):
        essenceID += tier[essence['tier']] + ' '
      essenceID += 'Essence of ' + essence['name']
      print('OK: ' + str(r.status_code) + essenceID)
      data.append(OrderedDict([
        ('id', essence['name'] + str(essence['tier'])),
        ('json', json.loads(r.text))
        ]))
    else:
      print('ERR: ' + str(r.status_code) + essenceID)

  with open('./src/essence_data.json', 'w+') as out:
    json.dump(data, out)

essenceData_data = open('./src/essence_data.json').read()
essenceData = json.loads(essenceData_data)

output = []
for essence in essenceData:
  rawText = essence['json']['query']['data'][3]['dataitem'][0]['item']
  essenceText = re.compile('<br ?/?>').split(rawText)
  trimmedText = []
  for text in essenceText:
    trimmedText.append(text.strip())
  output.append({ text: trimmedText})
  out = OrderedDict([
      ('id', essence['id']),
      ('text', trimmedText),
    ])

with open('./out/essenceText.json', 'w+') as out:
  json.dump(output, out)