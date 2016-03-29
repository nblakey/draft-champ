from django import forms
from .models import Team, DraftPick, Player

class NumberOfTeamsForm(forms.Form):
	numbers = (
		('4', '4'),
		('6', '6'),
		('8', '8'),
		('10', '10'),
		('12', '12'),
		('14', '14'),
		('16', '16'),
	)

	number_of_teams = forms.ChoiceField(label="Number of fantasy teams", choices=numbers)

class RostersForm(forms.Form):
	qbs = forms.IntegerField(label="QB", max_value=9)
	rbs = forms.IntegerField(label="RB", max_value=9)
	wrs = forms.IntegerField(label="WR", max_value=9)
	tes = forms.IntegerField(label="TE", max_value=9)
	defs = forms.IntegerField(label="DEF", max_value=9)
	ks = forms.IntegerField(label="K", max_value=9)
	rbwrs = forms.IntegerField(label="RB/WR", max_value=9)
	flexs = forms.IntegerField(label="FLEX", max_value=9)
	ops = forms.IntegerField(label="OP", max_value=9)
	bes = forms.IntegerField(label="BE")

class CreateFantasyTeamForm(forms.Form):
	team_name = forms.CharField(max_length=50, required=True)
	owner_first_name = forms.CharField(max_length=50)
	owner_last_name = forms.CharField(max_length=50)
	owner_email = forms.CharField(max_length=50)
	owner_draft_position = forms.IntegerField(max_value=16)

class KeeperForm(forms.Form):
	team = forms.ModelChoiceField(queryset=Team.objects.all())
	player = forms.ModelChoiceField(queryset=Player.objects.filter(available=True).order_by('last_name'))