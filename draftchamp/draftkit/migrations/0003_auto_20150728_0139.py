# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftkit', '0002_nflteam_abbrev'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='draft_order',
        ),
        migrations.AddField(
            model_name='draftpick',
            name='overall_pick_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='draft_order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
