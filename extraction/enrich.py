import json
import geolat2

stages = json.load(open('data/details.json'))
basics = json.load(open('data/basics.json'))
geocoded = json.load(open('data/geocoded.json'))

print('files loaded')

stages_dict = {s['num']:s for s in stages}

geocoded_count = 0
filiere_count = 0
niveau_count = 0


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
            #add country
            stage['country'] = addr.split("\n")[-1].strip()

            r = geocoded[addr]['results']
            if len(r) > 0:
                loc = r[0]['geometry']['location']
                lat = loc['lat']
                lng = loc['lng']
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
            or bl.startswith('Systèmes Complexes en Interaction'.lower()) \
            or bl.startswith('Innovation et Complexité'.lower()):
            branche_abbrev = "Master"
        elif bl.startswith('maintenance des'):
            branche_abbrev = "Licence Pro"
        else:
            #  branche_abbrev = "Autre"
            print("branche inconnue:", n,stage['branche'][:100])

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
            niveau_abbrev = "Master"
        elif 'apprenti' in nl:
            niveau_abbrev = "Apprentissage"
        elif 'intercul' in nl:
            niveau_abbrev = "TN07"
        elif 'licence' in nl:
            niveau_abbrev = "Licence Pro"
        elif 'hutech' in nl:
            niveau_abbrev = "HuTech"
        else:
            #niveau_abbrev = "Autre"
            print("niveau inconnu:", n,stage['niveau'][:30],)

    if niveau_abbrev != "":
        niveau_count += 1

    stage['branche_abbrev'] = branche_abbrev
    stage['niveau_abbrev'] = niveau_abbrev

    stage['filiere'] = filiere
    filiere_abbrev = ''

    fil = filiere.lower().strip()
    #GI
    if len(fil) > 1:
        if fil.startswith('Fouille de Données'.lower()):
            filiere_abbrev = 'FDD'
        elif fil.startswith('Systèmes et réseaux informatiques'.lower()):
            filiere_abbrev = 'SRI'
        elif fil.startswith('Aide à la décision en logistique'.lower()):
            filiere_abbrev = 'ADEL'
        elif fil.startswith("Ingénierie des connaissances et des supports".lower()):
            filiere_abbrev = 'ICSI'
        elif fil.startswith('systèmes temps-réel et informatique enfouie'.lower()):
            filiere_abbrev = 'STRI'
        #GB
        elif fil.startswith('Biomatériaux et biomécanique'.lower()):
            filiere_abbrev = 'BB'
        elif fil.startswith('Biomédical'.lower()):
            filiere_abbrev = 'BM'
        elif fil.startswith('conception et innnovation de bioproduits'.lower()):
            filiere_abbrev = 'CIB'
        elif fil.startswith('innovation aliments et agroressources'.lower()):
            filiere_abbrev = 'IAA'
        #GM
        elif fil.startswith('Acoustique et vibrations industrielles'.lower()):
            filiere_abbrev = 'AVI'
        elif fil.startswith('fiabilité-qualité industrielle'.lower()):
            filiere_abbrev = 'FQI'
        elif fil.startswith('Ingénierie du design industriel'.lower()):
            filiere_abbrev = 'IDI'
        elif fil.startswith('Matériaux et innovation technologique'.lower()):
            filiere_abbrev = 'MIT'
        elif fil.startswith('mécatronique, actionneurs, robotisation et systèmes'.lower()):
            filiere_abbrev = 'MARS'
        #GSM
        elif fil.startswith('Conception mécanique intégrée'.lower()):
            filiere_abbrev = 'CMI'
        elif fil.startswith('modélisation et optimisation des produits et structures'.lower()):
            filiere_abbrev = 'MOPS'
        elif fil.startswith('Production intégrée et logistique'.lower()):
            filiere_abbrev = 'PIL'
        #GSU
        elif fil.startswith("systèmes et réseaux pour l'environnement construit".lower()):
            filiere_abbrev = 'SR'
        elif fil.startswith('systèmes techniques intégrés'.lower()):
            filiere_abbrev = 'STI'
        elif fil.startswith('Aménagement et Ingénierie Environnementale'.lower()):
            filiere_abbrev = 'AIE'
        #GP
        elif fil.startswith('Qualité, Sécurité, Environnement'.lower()):
            filiere_abbrev = 'QSE'
        elif fil.startswith('Conduite des Procédés Industriels'.lower()):
            filiere_abbrev = 'CPI'
        elif fil.startswith('thermique-energétique'.lower()):
            filiere_abbrev = 'TE'
        elif fil.startswith('agro-industrie'.lower()):
            filiere_abbrev = 'AI'

        elif fil.startswith('Management des Projets Innovants'.lower()):
            filiere_abbrev = 'MPI'
        elif fil.startswith('Filière libre'.lower()):
            filiere_abbrev = 'Libre'
        else:
            print("Filiere inconnue:", fil[:100])

    if filiere_abbrev != "":
        filiere_count += 1

    stage['company'] = stage['company'].strip()

    stage['filiere_abbrev'] = filiere_abbrev

    stage['sujet'] = stage['title'].strip()
    stage.pop('title',None)
    stage['semestre'] = stage['semester']
    stage.pop('semester',None)
    stage.pop('semestre_annee',None)
    stage.pop('stage_reel',None)

    stage['semestre_annee'] = int(stage['semestre'][1:])
    stage['semestre_trimestre'] = stage['semestre'][0]

print('geocoded',geocoded_count,"/",len(basics))
print('filiere abbrev found',filiere_count,"/",len(basics))
print('niveau abbrev found',niveau_count,"/",len(basics))
json.dump(basics, open('data/enriched.json','w'), indent=2)
