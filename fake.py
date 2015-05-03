import csv

from faker import Faker
fake = Faker(locale="fr_FR")
#fake.seed(42)

myfile = open("data/fake.csv", 'w')
wr = csv.writer(myfile)
wr.writerow([x.strip() for x in "num, addresse, branche, filiere," \
        "company, description, etudiant, niveau," \
        "semestre, sujet, tuteur, done,confidentiel, country, city".split(',')])
for _ in range(4000):
    num = fake.random_int(min=0, max=9999)
    addresse = fake.street_address()+"\n"+str(fake.random_int(min=0, max=7000)) \
        +" "+fake.city()+"\n"+fake.country().upper()
    branche = fake.random_element(('Informatique','Mécanique','Tronc Commun'))
    done = fake.random_element(('x', 'x',' '))
    confidentiel = fake.random_element((' ', ' ',' ','x', ' '))
    filiere = fake.sentence(nb_words=5)
    company = fake.company()
    description = fake.text()
    etudiant = fake.name()
    niveau = fake.random_element(('ouvrier','projet de fin d\'étude','stage ouvrier'))
    country = fake.country().upper()
    city = fake.city()
    semestre = fake.random_element(('A','P'))+str(fake.random_int(min=2002, max=2015))
    sujet = fake.sentence(nb_words=6, variable_nb_words=True)
    tuteur = fake.name()
    wr.writerow((num, addresse, branche, filiere,
        company, description, etudiant, niveau,
        semestre, sujet, tuteur, done,confidentiel, country, city))
