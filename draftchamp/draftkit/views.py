from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import DraftPick, Team, Player

# Create your views here.
def index(request):
	draft_pick_list = DraftPick.objects.order_by('draft_round', 'pick_number')
	team_list = Team.objects.all()
	player_list = Player.objects.order_by('overall_rank')
	template = loader.get_template('draftkit/index.html')
	context = RequestContext(request, {
		'draft_pick_list': draft_pick_list,
		'team': team_list,
		'player_list': player_list
	})
	return HttpResponse(template.render(context))