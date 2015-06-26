# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nflteam',
            name='abbrev',
            field=models.CharField(default=b'XXX', max_length=3),
        ),
    ]
