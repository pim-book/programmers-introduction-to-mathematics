import json

with open('all_stories.json', 'r') as infile:
    data = json.loads(infile.read())

allWords = set()
for entry in data:
    allWords |= set(entry['words'])

print('{} unique words in all the stories'.format(len(allWords)))
print('{} documents total'.format(len(data)))
