import json
import geolat2

stages = json.load(open('data/details.json'))
basics = json.load(open('data/basics.json'))
geocoded = json.load(open('data/geocoded.json'))
geocoded_simple = json.load(open('data/geocoded3_cold.json'))

print('files loaded')

stages_dict = {s['num']:s for s in stages}

geocoded_count = 0

for stage in basics:
    n = None
    stage['confidentiel'] = False
    try:
        n = int(stage['num'])
    except:
        stage['confidentiel'] = True
    if n in stages_dict:
        stage.update(stages_dict[n])
    if 'done' not in stage:
        stage['done'] = False #TODO: what ? comment je peut savoir...
    if 'title' not in stage:
        print(stage)

    #add lat,lng
    addr = stage.get('addresse')
    lat = None
    lng = None
    if addr:
        if addr in geocoded:
            r = geocoded[addr]['results']
            if len(r) > 0:
                loc = r[0]['geometry']['location']
                lat = loc['lat']
                lng = loc['lng']
        try:
            simple_addr = geolat2.simplify(addr)
            if lat == None and simple_addr in geocoded_simple:
                #TODO:if FRANCE verify context is FRANCE, US, GRANDE BRETAGNE,...
                r = geocoded_simple[simple_addr]['features']
                if len(r) > 0:
                    loc = r[0]['center']
                    lng,lat = loc
        except Exception as e:
            print(e)
    if lat != None: 
        geocoded_count += 1

    stage['lat'] = lat
    stage['lng'] = lng

    #add branch, niveau, semester, filiere,...
    branche_abbrev = ""
    filiere = ""
    if 'branche' in stage:
        bl = stage['branche'].lower()
        if bl.startswith('inform') \
            or bl.startswith('Ingénierie des Services et des Systèmes'.lower()) \
            or bl.startswith("Sciences et Technologies de l'Information".lower()):
            branche_abbrev = "GI"
        elif bl.startswith('Mécanique, Option Génie des Systèmes Mécaniques'.lower()):
            branche_abbrev = "GSM"
        elif bl.startswith('mécan'):
            branche_abbrev = "GM"
        elif bl.startswith('tronc'):
            branche_abbrev = "TC"
        elif bl.startswith('génie biologique'):
            branche_abbrev = "GB"
        elif bl.startswith('génie des procédés'):
            branche_abbrev = "GP"
        elif bl.startswith('systèmes urbains'):
            branche_abbrev = "GSU"
        elif bl.startswith('Humanités et Technologie'.lower()):
            branche_abbrev = "HuTech"
        elif bl.startswith('Transformation et Valorisation'.lower()) \
            or bl.startswith('Systèmes Complexes en Interaction'.lower()):
            branche_abbrev = "Master"
        elif bl.startswith('maintenance des'):
            branche_abbrev = "Licence Pro"
        else:
            branche_abbrev = "autre"
            print("branche inconnue:", n,stage['branche'][:50])

        splitted = stage['branche'].split('filière',2)
        if len(splitted) > 1:
            filiere = splitted[-1].strip()

    niveau_abbrev = ""
    if 'niveau' in stage:
        nl = stage['niveau'].lower()
        if 'assistant' in nl:
            niveau_abbrev = "TN09"
        elif 'ouvrier' in nl:
            niveau_abbrev = "TN05"
        elif 'fin' in nl:
            niveau_abbrev = "TN10"
        elif 'master' in nl:
            niveau_abbrev = "master"
        elif 'apprenti' in nl:
            niveau_abbrev = "apprentissage"
        elif 'intercul' in nl:
            niveau_abbrev = "interculturel"
        elif 'licence' in nl:
            niveau_abbrev = "licence"
        elif 'hutech' in nl:
            niveau_abbrev = "hutech"
        else:
            niveau_abbrev = "autre"
            print("niveau inconnu:", n,stage['niveau'][:30],)

    stage['branche_abbrev'] = branche_abbrev
    stage['niveau_abbrev'] = niveau_abbrev

    stage['filiere'] = filiere

    stage['sujet'] = stage['title']
    stage.pop('title',None)
    stage['semestre'] = stage['semester']
    stage.pop('semester',None)
    stage.pop('semestre_annee',None)
    stage.pop('stage_reel',None)

    stage['semestre_annee'] = int(stage['semestre'][1:])
    stage['semestre_trimestre'] = stage['semestre'][0]

print('geocoded',geocoded_count,"/",len(basics))
json.dump(basics, open('data/enriched.json','w'), indent=2)
