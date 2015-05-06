import requests, json, collections

stages = json.load(open('data/details.json'))
addrs = collections.Counter([s['addresse'] for s in stages])

geocoded = json.load(open('data/geocoded.json'))

for addr,n in addrs.most_common():
    if addr in geocoded and len(geocoded[addr]['results']) != 0:
        continue
    print(len(geocoded),'/',len(addrs))
    print("geocode:\n",addr)
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address':addr,
        'sensor':'false',
        'key':'AIzaSyAr1Dk4AkBo44iIwOuG0zkDosRdjV0CG3I',
    }
    r = requests.get(url, params=params).json()
    geocoded[addr] = r
    if len(r['results']):
        print(r)
    with open('data/geocoded','w') as f:
        json.dump(geocoded,f,indent=2)
    with open('data/geocoded_backup','w') as f:
        json.dump(geocoded,f,indent=2)
