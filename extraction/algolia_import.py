from algoliasearch import algoliasearch as al
client = al.Client("X",'Y')
index = client.init_index('stages')

import json
stages = json.load(open('data/enriched.json'))
print('data loaded')

array = []
for i, row in enumerate(stages) :
    row['objectID'] = i
    array.append(row)
    if len(array) == 4000:
        print(i,"/",len(stages))
        index.save_objects(array)
        array = []
index.save_objects(array)
