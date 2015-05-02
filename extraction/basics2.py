import re
import json
from bs4 import BeautifulSoup
import csv

stages = json.load(open('data/basics.json'))

f = open('data/basics.csv','w', newline='')
w = csv.writer(f)

w.writerow([
    'num',
    'title',
    'city',
    'semester',
    'company',
    'country',
    ])

for stage in stages:
    w.writerow([
        stage['num'],
        stage['title'],
        stage['city'],
        stage['semester'],
        stage['company'],
        stage['country'],
        ])

nums = []
for stage in stages:
    n = stage['num']
    if n:
        try:
            nums.append(int(n))
        except:
            print('fail',n)

open('data/nums_to_do','w').write('\n'.join([str(n) for n in sorted(nums)]))


