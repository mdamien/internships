script = '/home/bob/prog/pores/carmen/scripts/carmen.js' \
    + ' --geojson '

import json, collections,random
from subprocess import *

def simplify(addr):
    city,country = addr.split('\n')[-2],addr.split('\n')[-1]
    _, city = city.split(' ',1)
    return city + " "+country

def main():
    stages = json.load(open('data/details.json'))
    addrs = collections.Counter([s['addresse'] for s in stages])

    geocoded = json.load(open('data/geocoded3.json'))

    for addr,n in addrs.most_common():
        try:
            addr = simplify(addr)
            if addr in geocoded:
                continue
            print(len(geocoded),'/',len(addrs.keys()))

            print("geocode:\n",addr)

            output = Popen(script.split()+['--query="{query}"'.format(query=addr)]
                , stdout=PIPE).communicate()[0]
            output = output.decode('utf-8')
            r =  json.loads(output)
            print(r['features'][0]['context'])
            geocoded[addr] = r

            with open('data/geocoded3.json','w') as f:
                json.dump(geocoded,f,indent=2)
            with open('data/geocoded3_cold.json','w') as f:
                json.dump(geocoded,f,indent=2)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()