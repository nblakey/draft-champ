from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.mail import send_mail
from .models import DraftPick, Team, Player, Owner
from .forms import NumberOfTeamsForm, RostersForm, CreateFantasyTeamForm, KeeperForm
from django.views.decorators.csrf import csrf_exempt
import json, requests, math

# Create your views here.
def setup(request):
	template = loader.get_template('draftkit/setup.html')
	number_teams_form = NumberOfTeamsForm()
	roster_setup_form = RostersForm()
	create_team_form = CreateFantasyTeamForm()
	context = RequestContext(request, {
		'number_teams_form': number_teams_form,
		'roster_setup_form': roster_setup_form,
		'create_team_form': create_team_form
	})
	return HttpResponse(template.render(context))

def keepers(request):
	picks_list = DraftPick.objects.all()
	highest_round = 1
	possible_rounds = []

	for pick in picks_list:
		if pick.draft_round > highest_round:
			highest_round = pick.draft_round

	for number in range(1, highest_round + 1):
		possible_rounds.append(number)

	teams_list = Team.objects.all()
	template = loader.get_template('draftkit/keepers.html')
	keeper_picks_form = KeeperForm()
	context = RequestContext(request, {
		'teams_list': teams_list,
		'keeper_picks_form': keeper_picks_form,
		'draft_rounds': possible_rounds
	})
	return HttpResponse(template.render(context))

def big_board(request):
	player_list_all = Player.objects.order_by('overall_rank')
	player_list_qb = Player.objects.filter(position='QB').order_by('overall_rank')
	player_list_rb = Player.objects.filter(position='RB').order_by('overall_rank')
	player_list_wr = Player.objects.filter(position='WR').order_by('overall_rank')
	player_list_te = Player.objects.filter(position='TE').order_by('overall_rank')
	player_list_def = Player.objects.filter(position='DEF').order_by('overall_rank')
	player_list_k = Player.objects.filter(position='K').order_by('overall_rank')
	teams_list = Team.objects.order_by('draft_order')
	template = loader.get_template('draftkit/big-board.html')
	context = RequestContext(request, {
		'player_list_all': player_list_all,
		'player_list_qb': player_list_qb,
		'player_list_rb': player_list_rb,
		'player_list_wr': player_list_wr,
		'player_list_te': player_list_te,
		'player_list_def': player_list_def,
		'player_list_k': player_list_k,
		'teams_list': teams_list
	})
	return HttpResponse(template.render(context))

@csrf_exempt
def make_pick(request, overall_pick):
	if request.GET:
		player_index = request.GET.get('player')
		drafted_player = Player.objects.get(id=player_index)
		pick_copy = {}
		try:
			if drafted_player.available:
				drafted_player.available = False
				drafted_player.save()

				pick = DraftPick.objects.get(overall_pick_number=overall_pick)
				pick_copy = pick
				pick.player = drafted_player
				pick.save()

				response = {
					'status': 1,
					'message': 'Player successfully drafted'
				}

			else:
				print("Player was already drafted!")

		except ValueError:
			response = {
				'status': 0,
				'message': 'Something went wrong'
			}	

	#Send email to owners with valid email addresses
	email_list = []
	sender_email = 'DraftChamp Fantasy Football App <blakeyn09@gmail.com>'
	message_body = 'Round ' + str(pick_copy.draft_round) + ', Pick ' + str(pick_copy.pick_number) + ' - ' + pick_copy.fantasy_team.owner.first_name + ' selects ' + pick_copy.player.first_name + ' ' + pick_copy.player.last_name + ', ' + pick_copy.player.position + ' (' + pick_copy.player.nfl_team + ')'
	all_owners = Owner.objects.all()
	for owner in all_owners:
		if '@' in owner.email: 
			email_list.append(owner.email)
	send_mail('', message_body, sender_email, email_list, fail_silently=False)

	return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def create_teams(request):
	if request.GET:
		roster_size = request.GET.get('rosterSize')
		teams_json = request.GET.get('teams')
		create_players_bool = request.GET.get('trigger')
		teams_list = json.loads(teams_json)
		ordered_teams_list = []

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
			)

			owner.save()
			owner_id = Owner.objects.get(id=owner.id)

			new_team = Team.objects.create(
				name = team_name,
				owner = owner_id,
				draft_order = owner_order
			)

			new_team.save()
			ordered_teams_list.append(new_team.id)

		reversed_teams_list = list(reversed(ordered_teams_list))

		create_picks(ordered_teams_list, reversed_teams_list, roster_size)

		response = {
			'status': 1,
			'message': 'Teams successfully created'
		}

		if create_players_bool == 'True':
			print("Creating players")
			create_players()
		return HttpResponse(json.dumps(response), content_type="application/json")

def create_picks(ordered_teams_list, reversed_teams_list, number_of_rounds):
	number_of_teams = len(ordered_teams_list)
	total_number_of_picks = number_of_teams * int(number_of_rounds)

	for overall_pick in range(1, total_number_of_picks + 1):
		if overall_pick % number_of_teams == 0:
			pick_number = number_of_teams
		else:
			pick_number = overall_pick % number_of_teams

		round_number = int(math.ceil(overall_pick / float(number_of_teams)))

		# If odd round number, use ordered list
		if bool(round_number % 2):
			team_id = ordered_teams_list[pick_number - 1]
		else:
			team_id = reversed_teams_list[pick_number - 1]

		fantasy_team = Team.objects.get(id=team_id)

		try:
			new_pick = DraftPick.objects.create(
				overall_pick_number = overall_pick,
				draft_round = round_number,
				pick_number = pick_number,
				fantasy_team = fantasy_team
			)
			new_pick.save()
		except ValueError:
			print("Didn't like that!")

def create_players():
	players_json = requests.get('http://www.fantasyfootballnerd.com/service/draft-rankings/json/uh5wdhaxa8kp/0/', auth=('blakeyn09', 'Nb63091!'))
	players = players_json.json()
	rankings = players['DraftRankings']

	for player in rankings:
		new_player = Player.objects.create(
			first_name = player['fname'],
			last_name = player['lname'],
			position = player['position'],
			position_rank = player['positionRank'],
			overall_rank = player['overallRank'],
			available = True,
			nfl_team = player['team']
		)
		new_player.save()

def trade_pick(request):
	if request.GET:
		team_1_id = request.GET.get('team1')
		team_2_id = request.GET.get('team2')
		round_1 = request.GET.get('round1')
		round_2 = request.GET.get('round2')

		team_1 = Team.objects.get(id=team_1_id)
		team_2 = Team.objects.get(id=team_2_id)

		team_1_picks = DraftPick.objects.filter(fantasy_team__id=team_1_id, draft_round=round_1).order_by('-id')
		team_2_picks = DraftPick.objects.filter(fantasy_team__id=team_2_id, draft_round=round_2).order_by('-id')

		if team_1_picks:
			pick_1 = team_1_picks[0]
		else:
			response = {
				'status': 2
			}

		if team_2_picks:
			pick_2 = team_2_picks[0]
		else:
			response = {
				'status': 3
			}
				
		if 'pick_1' in locals() and 'pick_2' in locals():
			pick_1.fantasy_team = team_2
			pick_1.save()

			pick_2.fantasy_team = team_1
			pick_2.save()

			response = {
				'status': 1
			}

	return HttpResponse(json.dumps(response), content_type="application/json")

def keep_pick(request):
	if request.GET:
		team_id = request.GET.get('team')
		player_id = request.GET.get('player')
		draft_round = request.GET.get('draft_round')

		team = Team.objects.get(id=team_id)
		player = Player.objects.get(id=player_id)

		draft_picks_in_round = DraftPick.objects.filter(fantasy_team__id=team_id, draft_round=draft_round).order_by('-id')

		if draft_picks_in_round:
			for index, picks in enumerate(draft_picks_in_round):
				if draft_picks_in_round[index].player is None:
					pick = draft_picks_in_round[index]
					break

		if 'pick' in locals():
			pick.player = player
			pick.save()

			player.available = False
			player.save()

			response = {
				'status': 1
			}
		else:
			response = {
				'status': 2
			}

	return HttpResponse(json.dumps(response), content_type="application/json")

def recent_picks(request):
	if request.GET:
		pick_number = int(request.GET.get('current_pick'))
		last_draft_pick = DraftPick.objects.order_by('-id')[0].overall_pick_number

		current_pick = DraftPick.objects.get(overall_pick_number=pick_number)

		if pick_number > 1:
			last_pick = DraftPick.objects.filter(overall_pick_number=pick_number-1)
		else:
			last_pick = None

		if pick_number < last_draft_pick:
			pick_number += 1
			next_pick = DraftPick.objects.filter(overall_pick_number=pick_number)

			if next_pick[0].player is not None:
				while next_pick[0].player is not None:
					if pick_number < last_draft_pick:
						pick_number += 1
						next_pick = DraftPick.objects.filter(overall_pick_number=pick_number)
		else:
			next_pick = None

		current_pick_team = current_pick.fantasy_team.name
		current_pick_round = current_pick.draft_round
		current_pick_pick = current_pick.pick_number

		if last_pick:
			last_pick_team = last_pick[0].fantasy_team.name
			last_pick_player = last_pick[0].player.first_name + " " + last_pick[0].player.last_name + ", " + last_pick[0].player.position + " (" + last_pick[0].player.nfl_team + ")"

			if next_pick:		
				next_pick_team = next_pick[0].fantasy_team.name
				next_pick_round = next_pick[0].draft_round
				next_pick_pick = next_pick[0].pick_number

				#If there is a last and next pick
				response = {
					'current_pick_team': current_pick_team,
					'current_pick_round': current_pick_round,
					'current_pick_pick': current_pick_pick,
					'last_pick_team': last_pick_team,
					'last_pick_player': last_pick_player,
					'next_pick_team': next_pick_team,
					'next_pick_round': next_pick_round,
					'next_pick_pick': next_pick_pick,
					'next_pick_number': pick_number
				}
			else:
				#If there is a last pick, but no next pick
				response = {
					'current_pick_team': current_pick_team,
					'current_pick_round': current_pick_round,
					'current_pick_pick': current_pick_pick,
					'last_pick_team': last_pick_team,
					'last_pick_player': last_pick_player
				}
		elif next_pick:
			next_pick_team = next_pick[0].fantasy_team.name
			next_pick_round = next_pick[0].draft_round
			next_pick_pick = next_pick[0].pick_number

			#If there is a next pick, but no last pick
			response = {
				'current_pick_team': current_pick_team,
				'current_pick_round': current_pick_round,
				'current_pick_pick': current_pick_pick,
				'next_pick_team': next_pick_team,
				'next_pick_round': next_pick_round,
				'next_pick_pick': next_pick_pick,
				'next_pick_number': pick_number
			}


	return HttpResponse(json.dumps(response), content_type="application/json")

def show_roster(request):
	if request.GET:
		position_list = request.GET.getlist('roster[]')
		team_id = request.GET.get('team')
		roster = [None] * len(position_list)

		selected_team = Team.objects.get(id=team_id)
		picks_by_selected_team = DraftPick.objects.filter(fantasy_team=selected_team).order_by('id')

		for index, pick in enumerate(picks_by_selected_team):
			if picks_by_selected_team[index].player:
				open_slot = find_open_roster_slot(picks_by_selected_team[index].player.position, position_list, roster)
				player = picks_by_selected_team[index].player
				roster[open_slot] = player.first_name + " " + player.last_name + " (" + player.nfl_team + ") - Round " + str(pick.draft_round)

		response = {
			'roster': roster
		}

	return HttpResponse(json.dumps(response), content_type="application/json")

def find_open_roster_slot(position, position_list, roster):
	for index, pos in enumerate(position_list):
		if position == pos and roster[index] == None:
			return index
		elif position_fits_slot(position, pos) and roster[index] == None:
			return index

def position_fits_slot(position1, position2):
	if position1 == 'QB':
		if position2 == 'OP' or position2 == 'BE':
			return True

	elif position1 == 'RB' or position1 == 'WR':
		if position2 == 'RB/WR' or position2 == 'FLEX' or position2 == 'OP' or position2 == 'BE':
			return True

	elif position1 == 'TE':
		if position2 == 'FLEX' or position2 == 'OP' or position2 == 'BE':
			return True
	
	return False

