import json, csv

details = json.load(open('data/enriched.json'))

print('files loaded')

data = details

######## STAGES.CSV

out = open('data/stages.csv', 'w', newline='')
w = csv.writer(out)

header = list(sorted(data[0].keys()))
print(header)
w.writerow(header)

def get(s, key):
    if key in ('done','confidentiel'):
        return 'x' if s[key] else ''
    return s.get(key)

for attrs in data:
    w.writerow([get(attrs,x) for x in header])

print("stages.csv done")




out = open('data/stages_mini.csv', 'w', newline='')
w = csv.writer(out)

header = list(sorted(data[0].keys()))
print(header)
w.writerow(header)

def get(s, key):
    if key in ('done','confidentiel'):
        return 'x' if s[key] else ''
    return s.get(key)

for attrs in data[:3000]:
    w.writerow([get(attrs,x) for x in header])

print("stages_mini.csv done")




print('Map csv')
out = open('data/stages_coords.csv', 'w', newline='')
w = csv.writer(out)

header = 'id,lat,lng,sujet,company,country,semestre_annee,semestre_trimestre,done,niveau_abbrev,branche_abbrev'
header = header.split(',')

print(header)
w.writerow(header)

for attrs in data:
    w.writerow([get(attrs,x) for x in header])

print('stages_coords done')