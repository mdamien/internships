import re
import json
from bs4 import BeautifulSoup
import csv


text = open('data/all.html',encoding="windows-1252").read()

stages = []
for match in re.findall(r'<tr class="i?m?pair.*?</tr', text, re.DOTALL):
    stages.append(match)

print('all.html parsed')

l = []
c = 0
for i,stage in enumerate(stages):
    try:
        soup = BeautifulSoup(stage)
        semester, title, company, _, city, country_code, _ = [x.text for x in soup.findAll('td')]
        o = soup.find('tr').attrs.get('onclick','')
        for td in soup.findAll('td'):
            if 'title' in td.attrs:
                country = td.attrs['title']
        if o == '':
            print("pas de num:",company)
            c += 1
        num = o.replace('ouvreStage(','').replace(');','')
        l.append({
            'num':num,
            'semester':semester,
            'country':country,
            'company':company,
            'city':city,
            'title':title,
            #use country code / abbrev ?
            })
    except Exception as e:
        print(stage)
        raise e from 'oops'
    if i % 100 == 0:
        print(i,'/',len(stages))
print(c,"stages sans num")
json.dump(l, open('data/basics.json','w'), indent=4)

print("basics.json finished")

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


