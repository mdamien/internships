from django.shortcuts import render

from .models import Stage

from collections import Counter
import json
import itertools

from django.contrib.auth.decorators import login_required

import watson

def distinct(value):
    yield ('all','Tous')
    the_set = set()
    for s in Stage.objects.values(value).distinct():
        x = s[value]
        if x and x not in the_set:
            yield (x,x)
            the_set.add(x)

def search(request):
    context = {}
    context['count_all'] = Stage.objects.all().count()
    context['page'] = 'search'
    context['show_map'] = 'map' in request.GET

    def distinct_sem():
        the_set = set()
        for s in Stage.objects.values('semestre','semestre_annee').distinct():
            x = s['semestre'] + str(s['semestre_annee'])
            if x not in the_set:
                yield (x,x)
                the_set.add(x)

    choices = {}
    choices['niveau'] = distinct('niveau_abbrev')
    choices['branche'] = distinct('branche_abbrev')
    choices['semestre'] = list(distinct_sem())
    context['choices'] = choices

    results = Stage.objects.all().defer('description','etudiant','tuteur',
        'filiere','niveau','branche')

    niveau = request.GET.get('niveau',None)
    if niveau and niveau != "all":
        results = results.filter(niveau_abbrev=niveau)

    branche = request.GET.get('branche',None)
    if branche and branche != "all":
        results = results.filter(branche_abbrev=branche)

    not_taken = request.GET.get('not_taken',None)
    if not_taken == None:
        print('only taken filtering!')
        results = results.filter(done=True)

    sem_from = request.GET.get('from',None)
    if sem_from:
        from_sem = sem_from[0]
        from_annee = int(sem_from[1:])
        results = results.filter(semestre_annee__gte=from_annee, \
            semestre__lte=from_sem)

    sem_to = request.GET.get('to',None)
    if sem_to:
        to_sem = sem_to[0]
        to_annee = int(sem_to[1:])
        results = results.filter(semestre_annee__lte=to_annee, \
            semestre__gte=to_sem)

    q = request.GET.get('q',None)
    if q and q != "" and q != None:
        results = [x.object for x in
            watson.search(q, models=(results,),ranking=False)]
        results.sort(key=lambda x:x.semestre)
        results.sort(key=lambda x:-x.semestre_annee)

    context['nb_results'] = len(results)

    if context['show_map']:
        objects = [{
            'lat':s.lat,
            'lng':s.lng,
            'sujet':s.sujet,
            'url':s.get_absolute_url(),
            'pk':s.pk,
        } for s in results]
        context['map_json'] = json.dumps(objects)
    else:
        results = list(results)[:200]

    context['results'] = results
    return render(request,'stages/search.html',context)

def details(request,id):
    context = {}
    context['count_all'] = Stage.objects.all().count()

    id = int(id)
    stage = Stage.objects.get(num=id)
    if not stage:
        stage = Stage.objects.get(pk=id)
    context['stage'] = stage

    return render(request,'stages/details.html',context)

def stats(request):
    context = {}
    context['count_all'] = Stage.objects.all().count()
    context['page'] = 'stats'

    stages = reversed(list(Stage.objects.all().only(
        'semestre','semestre_annee','done','confidentiel','branche_abbrev')))


    branches = [x for x,_ in distinct('branche_abbrev') if x != 'all']

    data = {
        'semesters':[],
        'done':[],
        'all':[],
        'branches':{b:[] for b in branches},
    }


    for sem, g in itertools.groupby(stages, lambda x:x.full_semester()):
        if sem == "A2015":
            continue
        data['semesters'].append(sem)
        all,done = 0,0
        branches = {b:0 for b in branches}
        for s in g:
            if s.done:
                done += 1
                if s.branche_abbrev != "":
                    branches[s.branche_abbrev] += 1
            all += 1
        for br in branches:
            data['branches'][br].append(branches[br])
        data['done'].append(done)
        data['all'].append(all)
    context['stats_semesters'] = json.dumps(data)

    return render(request,'stages/stats.html',context)