# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0004_auto_20150802_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftpick',
            name='fantasy_team',
            field=models.ForeignKey(to='draftkit.Team', blank=True),
        ),
        migrations.AlterField(
            model_name='draftpick',
            name='player',
            field=models.ForeignKey(to='draftkit.Player', blank=True),
        ),
    ]
