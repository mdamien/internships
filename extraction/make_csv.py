import json, csv

details = json.load(open('data/enriched.json'))

print('files loaded')

data = details

######## STAGES.CSV

out = open('../data/stages.csv', 'w', newline='')
w = csv.writer(out)

header = list(sorted(data[0].keys()))
print(header)
w.writerow(header)

def get(s, key):
    if key in ('done','confidentiel'):
        return 'x' if s[key] else ''
    return s.get(key)

done = set()
for attrs in data:
    w.writerow([get(attrs,x) for x in header])

print("stages.csv done")





out = open('../data/stages_done.csv', 'w', newline='')
w = csv.writer(out)

header = list(data[0].keys())
print(header)
w.writerow(header)

for attrs in data:
    if attrs['done']:
        w.writerow([get(attrs,x) for x in header])

print("stages_done.csv done")




import random;random.shuffle(data)
data = data[:3000]

out = open('../data/stages_mini.csv', 'w', newline='')
w = csv.writer(out)

header = list(data[0].keys())
print(header)
w.writerow(header)

for attrs in data:
    w.writerow([get(attrs,x) for x in header])

print("stages_mini.csv done")