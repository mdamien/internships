from django.db import models

from django.core.urlresolvers import reverse

class Stage(models.Model):
    addresse = models.TextField()
    branche = models.CharField(max_length=100)
    branche_abbrev = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    entreprise = models.CharField(max_length=200)
    confidentiel = models.BooleanField()
    pays = models.CharField(max_length=50)
    description = models.TextField()
    done = models.BooleanField()
    etudiant = models.CharField(max_length=200)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    niveau = models.CharField(max_length=20)
    niveau_abbrev = models.CharField(max_length=100)
    num = models.IntegerField(null=True)
    semestre = models.CharField(max_length=100)
    semestre_annee = models.IntegerField()
    sujet = models.CharField(max_length=200)
    tuteur = models.CharField(max_length=100)
    filiere = models.CharField(max_length=100)

    def full_semester(self):
        return "{}{}".format(self.semestre, self.semestre_annee)

    def __str__(self):
        return "<{}> {}".format(self.num, self.sujet)

    def get_absolute_url(self):
        if self.num:
            return reverse('details', args=(self.num,))
        return reverse('details', args=(self.pk,))

    class Meta:
        ordering = ["-semestre_annee","semestre"]

import watson
watson.register(Stage)
