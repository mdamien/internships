# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stage',
            options={'ordering': ['semestre_annee', '-semestre']},
        ),
        migrations.AddField(
            model_name='stage',
            name='filiere',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
