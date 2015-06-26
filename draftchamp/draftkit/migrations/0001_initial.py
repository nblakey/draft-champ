# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DraftPick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft_round', models.IntegerField()),
                ('pick_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NFLTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('draft_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=3, choices=[(b'QB', b'Quarterback'), (b'RB', b'Running back'), (b'WR', b'Wide receiver'), (b'TE', b'Tight end'), (b'DST', b'Defense'), (b'K', b'Kicker')])),
                ('position_rank', models.IntegerField()),
                ('overall_rank', models.IntegerField()),
                ('available', models.BooleanField(default=True, verbose_name=b'Available')),
                ('nfl_team', models.ForeignKey(to='draftkit.NFLTeam')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(to='draftkit.Owner')),
            ],
        ),
        migrations.AddField(
            model_name='draftpick',
            name='fantasy_team',
            field=models.ForeignKey(to='draftkit.Team'),
        ),
        migrations.AddField(
            model_name='draftpick',
            name='player',
            field=models.ForeignKey(to='draftkit.Player'),
        ),
    ]
