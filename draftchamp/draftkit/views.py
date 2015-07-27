from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import DraftPick, Team, Player, Owner
from .forms import NumberOfTeamsForm, CreateFantasyTeamForm
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def setup(request):
	template = loader.get_template('draftkit/setup.html')
	number_teams_form = NumberOfTeamsForm()
	create_team_form = CreateFantasyTeamForm()
	context = RequestContext(request, {
		'number_teams_form': number_teams_form,
		'create_team_form': create_team_form
	})
	return HttpResponse(template.render(context))

def big_board(request):
	draft_pick_list = DraftPick.objects.order_by('draft_round', 'pick_number')
	team_list = Team.objects.all()
	player_list = Player.objects.order_by('overall_rank')
	template = loader.get_template('draftkit/big-board.html')
	context = RequestContext(request, {
		'draft_pick_list': draft_pick_list,
		'team': team_list,
		'player_list': player_list
	})
	return HttpResponse(template.render(context))

@csrf_exempt
def make_pick(request, draft_round, pick_number):
	if request.GET:
		team_index = request.GET.get('team')
		player_index = request.GET.get('player')
		drafted_player = Player.objects.get(id=player_index)
		fantasy_team = Team.objects.get(id=team_index)
		print(drafted_player)
		print(fantasy_team)
		try:
			if drafted_player.available:
				drafted_player.available = False
				drafted_player.save()

				pick = DraftPick.objects.create(
					draft_round = draft_round,
					pick_number = pick_number,
					fantasy_team = fantasy_team,
					player = drafted_player
				)
				pick.save()
				response = {
					'status': 1,
					'message': 'Player successfully drafted'
				}
				return HttpResponse(json.dumps(response), content_type="application/json")

			else:
				print("Player was already drafted!")

		except ValueError:
			response = {
				'status': 0,
				'message': 'Something went wrong'
			}	

	return HttpResponse(response, content_type="application/json")

@csrf_exempt
def create_teams(request):
	if request.GET:
		teams_json = request.GET.get('teams')
		teams_list = json.loads(teams_json)
		for team in teams_list:
			team_name = team['teamName']
			owner_first = team['ownerFirst']
			owner_last = team['ownerLast']
			owner_email = team['ownerEmail']
			owner_order = team['ownerOrder']

			owner = Owner.objects.create(
				first_name = owner_first,
				last_name = owner_last,
				email = owner_email,
				draft_order = owner_order
			)

			owner.save()
			owner_id = Owner.objects.get(id=owner.id)

			new_team = Team.objects.create(
				name = team_name,
				owner = owner_id
			)

			new_team.save()
		response = {
			'status': 1,
			'message': 'Player successfully drafted'
		}
		return HttpResponse(json.dumps(response), content_type="application/json")

