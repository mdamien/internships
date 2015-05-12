# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('addresse', models.TextField()),
                ('branche', models.CharField(max_length=100)),
                ('branche_abbrev', models.CharField(max_length=50)),
                ('ville', models.CharField(max_length=50)),
                ('entreprise', models.CharField(max_length=200)),
                ('confidentiel', models.BooleanField()),
                ('pays', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('done', models.BooleanField()),
                ('etudiant', models.CharField(max_length=200)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
                ('niveau', models.CharField(max_length=20)),
                ('niveau_abbrev', models.CharField(max_length=100)),
                ('num', models.IntegerField(null=True)),
                ('semestre', models.CharField(max_length=100)),
                ('semestre_annee', models.IntegerField()),
                ('sujet', models.CharField(max_length=200)),
                ('tuteur', models.CharField(max_length=100)),
            ],
        ),
    ]
