from django.db import models

class Owner(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.CharField(max_length=30)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Team(models.Model):
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(Owner)
	draft_order = models.IntegerField()

	def __str__(self):
		return self.name

class Player(models.Model):
	POSITIONS = (
		('QB', 'Quarterback'),
		('RB', 'Running back'),
		('WR', 'Wide receiver'),
		('TE', 'Tight end'),
		('DEF', 'Defense'),
		('K', 'Kicker')
	)

	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	position = models.CharField(max_length=3, choices=POSITIONS)
	position_rank = models.IntegerField()
	overall_rank = models.IntegerField()
	available = models.BooleanField('Available', default=True)
	nfl_team = models.CharField(max_length=3)

	def __str__(self):
		return self.first_name + ' ' + self.last_name + ', ' + self.position + ' (' + self.nfl_team + ')'

class DraftPick(models.Model):
	draft_round = models.IntegerField(blank=True, null=True)
	pick_number = models.IntegerField(blank=True, null=True)
	overall_pick_number = models.IntegerField()
	fantasy_team = models.ForeignKey(Team, blank=True, null=True)
	player = models.ForeignKey(Player, blank=True, null=True)

	def __str__(self):
		return 'Round ' + str(self.draft_round) + ", Pick " + str(self.pick_number)

