from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from stages.models import Stage

from pprint import pprint as pp

import csv

"""
addresse,branche,branche_abbrev,city,company,
confidentiel,country,description,done,etudiant,lat,lng,niveau,
niveau_abbrev,num,semestre,semestre_annee,semestre_trimestre,sujet,tuteur
"""

def replace_key(d,old,new):
    d[new] = d[old]
    del d[old]

def apply_to_key(d,key,f):
    try:
        d[key] = f(d[key])
    except:
        d[key] = None

class Command(BaseCommand):

    args = "stages.csv"

    def handle(self, *args, **options):
        limit = int(args[1]) if len(args) == 2 else None
        previous_size = Stage.objects.all().count()
        Stage.objects.all().delete()
        print(previous_size,"stages deleted")
        with open(args[0]) as f:
            reader = csv.reader(open(args[0]))
            header = reader.__next__()
            try:
                to_insert = []
                for i,row in enumerate(reader):
                    data = {key:row[i] for i,key in enumerate(header)}
                    replace_key(data,'country','pays')
                    replace_key(data,'city','ville')
                    replace_key(data,'semestre_trimestre','semestre')
                    replace_key(data,'company','entreprise')
                    data['confidentiel'] = data.get('confidentiel') == 'x'
                    data['done'] = data.get('done') == 'x'     
                    apply_to_key(data,'num',int)
                    apply_to_key(data,'lat',float)
                    apply_to_key(data,'lng',float)
                    stage = Stage(**data)
                    to_insert.append(stage)
                    if i % 1000 == 1:
                        print('\b',i,'loaded')
                    if limit and i > limit:
                        break
                print('insertion....')
                Stage.objects.bulk_create(to_insert)
            except Exception as e:
                pp(data)
                raise e

        print(Stage.objects.all().count(),'stages inserted')