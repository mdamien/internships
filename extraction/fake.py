import csv

from faker import Faker
fake = Faker(locale="fr_FR")
#fake.seed(42)

myfile = open("data/fake.csv", 'w')
wr = csv.writer(myfile)
wr.writerow([x.strip() for x in "num, addresse, branche_abbrev, filiere," \
        "company, description, etudiant, niveau," \
        "semestre, semestre_annee, sujet, tuteur, done,confidentiel, country, city,lat,lng".split(',')])
for _ in range(500):
    num = fake.random_int(min=0, max=9999)
    addresse = fake.street_address()+"\n"+str(fake.random_int(min=0, max=7000)) \
        +" "+fake.city()+"\n"+fake.country().upper()
    branche_abbrev = fake.random_element(('GI','GM/GSM','GB'))
    done = fake.random_element(('x', 'x',' '))
    confidentiel = fake.random_element((' ', ' ',' ','x', ' '))
    filiere = fake.sentence(nb_words=5)
    company = fake.company()
    description = fake.text()
    etudiant = fake.name()
    niveau = fake.random_element(('ouvrier','projet de fin d\'étude','stage ouvrier'))
    country = fake.country().upper()
    city = fake.city()
    semestre = fake.random_element(('A','P'))
    semestre_annee = str(fake.random_int(min=2002, max=2015))
    sujet = fake.sentence(nb_words=6, variable_nb_words=True)
    lat = fake.latitude()
    lng = fake.longitude()
    tuteur = fake.name()
    wr.writerow((num, addresse, branche_abbrev, filiere,
        company, description, etudiant, niveau,
        semestre, semestre_annee, sujet, tuteur, done,
        confidentiel, country, city,lat,lng))
