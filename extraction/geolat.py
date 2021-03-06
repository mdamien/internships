import requests, json, collections, random

stages = json.load(open('data/details.json'))
addrs = collections.Counter([s['addresse'] for s in stages])

addrs = list(addrs.items())
random.shuffle(addrs)

geocoded = json.load(open('data/geocoded_cold.json'))

def google(addr):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address':addr.replace('\n',' - '),
        'sensor':'false',
        'key':'AIzaSyAr1Dk4AkBo44iIwOuG0zkDosRdjV0CG3I',
    }
    r = requests.get(url, params=params).json()
    geocoded[addr] = r
    if len(r['results']) == 0:
        print(r)
    return r

def geocoded_real(geocoded):
    return len([1 for x in geocoded if len(geocoded[x]['results']) != 0])

for addr,n in addrs:
    if addr in geocoded and len(geocoded[addr]['results']) != 0:
        continue
    print("geocoded:",len(geocoded),'/',len(addrs))
    print("really geocoded:",geocoded_real(geocoded),'/',len(geocoded))
    print("geocode:\n",addr,"\n","n:",n)
    google(addr)
    with open('data/geocoded.json','w') as f:
        json.dump(geocoded,f,indent=2)
    with open('data/geocoded_cold.json','w') as f:
        json.dump(geocoded,f,indent=2)
