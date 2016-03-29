# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0003_auto_20150728_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='nfl_team',
            field=models.CharField(max_length=3),
        ),
        migrations.DeleteModel(
            name='NFLTeam',
        ),
    ]
