# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0005_auto_20150802_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftpick',
            name='fantasy_team',
            field=models.ForeignKey(blank=True, to='draftkit.Team', null=True),
        ),
        migrations.AlterField(
            model_name='draftpick',
            name='player',
            field=models.ForeignKey(blank=True, to='draftkit.Player', null=True),
        ),
    ]
