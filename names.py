import json
from collections import OrderedDict

# load json
words_data = open('./src/Words.json').read()
words_json = json.loads(words_data)
tags_data = open('./src/Tags.json').read()
tags_json = json.loads(tags_data)
uniqueTags_data = open('./src/unique_base_tags.json').read()
uniqueTags_json = json.loads(uniqueTags_data)

# words
words_headers = []
for header in words_json[0]['header']:
  words_headers.append(header['name'])

words = []
for word in words_json[0]['data']:
  words.append(OrderedDict(zip(words_headers, word)))

# tags
tags = []
for tag in tags_json[0]['data']:
  tags.append(tag[0])

def getTags(word):
  wordTags = []
  for key in word['SpawnWeight_TagsKeys']:
    if (word['SpawnWeight_Values'][word['SpawnWeight_TagsKeys'].index(key)] > 0):
      if (tags[key] in uniqueTags_json):
        wordTags.append(tags[key])
  return wordTags

def parseWord(word):
  out = OrderedDict([
    ('text', word['Text']),
    ('type', word['WordlistsKey']),
    ('tags', getTags(word))
  ])
  return out

names = []
for word in words:
  names.append(parseWord(word))

### Filter unused
types = [1, 2]
names = [x for x in names if x['type'] in types and len(x['tags']) > 0]
###

### Restructure
nameTags = []
prefixes = []
suffixes = []
for name in names:
  for tag in name['tags']:
    if tag not in nameTags:
      nameTags.append(tag)
  if name['type'] == 1:
    prefixes.append(name)
  elif name['type'] == 2:
    suffixes.append(name)

namePrefixes = OrderedDict.fromkeys(nameTags)
for key in namePrefixes.keys():
  namePrefixes[key] = []
for name in prefixes:
  for tag in name['tags']:
    namePrefixes[tag].append(name['text'])

nameSuffixes = OrderedDict.fromkeys(nameTags)
for key in namePrefixes.keys():
  nameSuffixes[key] = []
for name in suffixes:
  for tag in name['tags']:
    nameSuffixes[tag].append(name['text'])

namesStructured = OrderedDict({ 'prefixes': namePrefixes, 'suffixes': nameSuffixes })
###

with open('./out/names.json', 'w+') as out:
  json.dump(namesStructured, out, ensure_ascii=False)