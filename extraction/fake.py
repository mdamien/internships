# -*- coding: utf-8 -*-

import csv

from faker import Faker
fake = Faker(locale="fr_FR")
#fake.seed(42)

myfile = open("data/fake2.csv", 'w')
wr = csv.writer(myfile)
wr.writerow([x.strip() for x in "num, addresse, branche_abbrev, filiere," \
        "company, description, etudiant, niveau," \
        "semestre, semestre_annee, sujet, tuteur, done,confidentiel, country, city,lat,lng".split(',')])
for i in range(20000):
    num = i #PK : can't be random (no duplicates allowed)
    addresse = fake.street_address()+"\n"+str(fake.random_int(min=0, max=7000)) \
        +" "+fake.city()+"\n"+fake.country().upper()
    branche_abbrev = fake.random_element(('GI','GM', 'GSM','GB', 'GSU', 'GP'))
    done = fake.random_element(('x', 'x', 'x', 'x', ' '))
    confidentiel = fake.random_element((' ', ' ',' ','x', ' '))
    filiere = fake.sentence(nb_words=3)
    company = fake.company()
    description = fake.text()
    etudiant = fake.name()
    niveau = fake.random_element(('assistant',u"projet de fin d\'étude",'stage ouvrier', 'apprentissage', 'interculturel'))
    country = fake.country().upper()
    city = fake.city()
    semestre = fake.random_element(('A','P'))
    semestre_annee = str(fake.random_int(min=2002, max=2015))
    sujet = fake.sentence(nb_words=6, variable_nb_words=True)
    lat = fake.latitude()
    lng = fake.longitude()
    tuteur = fake.name()
    wr.writerow((num, addresse.encode('utf-8'), branche_abbrev.encode('utf-8'), filiere.encode('utf-8'),
        company.encode('utf-8'), description.encode('utf-8'), etudiant.encode('utf-8'), niveau.encode('utf-8'),
        semestre.encode('utf-8'), semestre_annee, sujet.encode('utf-8'), tuteur.encode('utf-8'), done.encode('utf-8'),
        confidentiel.encode('utf-8'), country.encode('utf-8'), city.encode('utf-8'),lat,lng))
