# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0006_auto_20150802_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftpick',
            name='draft_round',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='draftpick',
            name='pick_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=3, choices=[(b'QB', b'Quarterback'), (b'RB', b'Running back'), (b'WR', b'Wide receiver'), (b'TE', b'Tight end'), (b'DEF', b'Defense'), (b'K', b'Kicker')]),
        ),
    ]
