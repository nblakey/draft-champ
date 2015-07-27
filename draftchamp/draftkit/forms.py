from django import forms

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

	number_of_teams = forms.ChoiceField(choices=numbers)

class CreateFantasyTeamForm(forms.Form):
	team_name = forms.CharField(max_length=50, required=True)
	owner_first_name = forms.CharField(max_length=50)
	owner_last_name = forms.CharField(max_length=50)
	owner_email = forms.CharField(max_length=50)
	owner_draft_position = forms.CharField(max_length=2)