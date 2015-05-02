import csv

from faker import Faker
fake = Faker(locale="fr_FR")
#fake.seed(42)

myfile = open("data/fake.csv", 'w')
wr = csv.writer(myfile)
wr.writerow([x.strip() for x in "num, addresse, branche_abbrev, filiere," \
        "company, description, etudiant, niveau_abbrev," \
        "semestre_annee, semestre, sujet, tuteur, stage_reel".split(',')])
for _ in range(2000):
    num = fake.random_int(min=0, max=9999)
    addresse = fake.street_address()+"\n"+str(fake.random_int(min=0, max=7000)) \
        +" "+fake.city()+"\n"+fake.country().upper()
    branche_abbrev = fake.random_element(('GI','GB','GP'))
    stage_reel = fake.random_element((True, False))
    filiere = fake.sentence(nb_words=5)
    company = fake.company()
    description = fake.text()
    etudiant = fake.name()
    niveau_abbrev = fake.random_element(('TN10','TN09','TN05'))
    semestre_annee = fake.year()
    semestre = fake.random_element(('A','P'))
    sujet = fake.sentence(nb_words=6, variable_nb_words=True)
    tuteur = fake.name()
    wr.writerow((num, addresse, branche_abbrev, filiere,
        company, description, etudiant, niveau_abbrev,
        semestre_annee, semestre, sujet, tuteur, stage_reel))
