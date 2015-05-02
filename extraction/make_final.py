import json, csv

details = json.load(open('data/details.json'))
basics = json.load(open('data/basics.json'))

out = open('../data/stages.csv', 'w', newline='')
w = csv.writer(out)

data = details

#header
header = "addresse,branche,branche_abbrev,company,description,etudiant,niveau" \
    ",niveau_abbrev,num,semestre,semestre_annee,sujet,tuteur".split(',')
print(header)
w.writerow(header)

#content
for attrs in data:
    if attrs["stage_reel"]:
        w.writerow(list(attrs[x] for x in header))

out.close()
print("stages.csv done")

out = open('../data/stages_all.csv', 'w', newline='')
w = csv.writer(out)

data = details

#header
header = list(data[0].keys())
print(header)
w.writerow(header)

#content
for attrs in data:
    w.writerow(list(attrs[x] for x in header))

print("stages_all.csv done")