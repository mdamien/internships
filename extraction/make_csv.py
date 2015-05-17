import json, csv,sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "stages.csv"
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else None

details = json.load(open('data/enriched.json'))

print('files loaded')

data = details

######## STAGES.CSV

out = open('data/'+OUT, 'w', newline='')
w = csv.writer(out)

header = list(sorted(data[0].keys()))
print(header)
w.writerow(header)

def get(s, key):
    if key in ('done','confidentiel'):
        return 'x' if s[key] else ''
    return s.get(key)

for i,attrs in enumerate(data):
    if LIMIT and i > LIMIT:
        break
    w.writerow([get(attrs,x) for x in header])

print("stages.csv done")