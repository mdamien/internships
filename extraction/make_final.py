import json, csv

details = json.load(open('data/details.json'))
details_failed = json.load(open('data/details_failed.json'))
basics = json.load(open('data/basics.json'))

print('files loaded')

########## merged.json

details_dict = {s['num']:s for s in details}
details_failed_dict = {s['n']:s for s in details_failed}

data = []
for stage in basics:
    n = None
    stage['confidentiel'] = False
    try:
        n = int(stage['num'])
    except:
        stage['confidentiel'] = True
    if n in details_dict:
        stage.update(details_dict[n])
    if 'done' not in stage:
        stage['done'] = False #TODO: what ? comment je peut savoir...
    stage['sujet'] = stage['title']
    stage.pop('title',None)
    stage['semestre'] = stage['semester']
    stage.pop('semestre_annee',None)
    stage.pop('stage_reel',None)
    stage.pop('niveau_abbrev',None)
    stage.pop('branche_abbrev',None)
    data.append(stage)

json.dump(data, open('data/merged.json','w'), indent=2)
print('merged.json done')

######## STAGES.CSV

out = open('../data/stages.csv', 'w', newline='')
w = csv.writer(out)

header = list(data[0].keys())
print(header)
w.writerow(header)

def get(s, key):
    if key in ('done','confidentiel'):
        return 'x' if s[key] else ''
    return s.get(key)

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