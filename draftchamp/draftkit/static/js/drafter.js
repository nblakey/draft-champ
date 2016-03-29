var $playerID,
	nextPick;

$(function() {
	$('form[name=draft-board]').submit(draftSelectedPlayer); 

	$('.player-position').click(function() {
		$('.select-player').addClass('hidden');
		$('.player-position').removeClass('unclickable');
	});
	$('.all-list').click(showAll);
	$('.qb-list').click(showQBs);
	$('.rb-list').click(showRBs);
	$('.wr-list').click(showWRs);
	$('.te-list').click(showTEs);
	$('.def-list').click(showDEFs);
	$('.k-list').click(showKs);

	$('.team-select-dropdown').change(showRoster);

	//Set pick and round number storage if we haven't yet
	if(!localStorage.getItem('overallPickNumber')) {
		localStorage['overallPickNumber'] = 1;
	}

	getRecentPicks();

});

function draftSelectedPlayer(e) {
	e.preventDefault();

	var $form = $(e.target);
	$playerID = $form.find('select option:selected')[0].id;

	var overallNumber = getPickNumber();

	var url = 'selection/'+overallNumber+'/';

	var data = {
		'player': $playerID
	}

	$.getJSON(url, data, function(response) {
		if(response.status == 1) {
			incrementPick();
			window.top.location.reload();
		}
	});
}

function getPickNumber() {
	return parseInt(localStorage.getItem('overallPickNumber'), 10);
}

function incrementPick() {
	localStorage['overallPickNumber'] = nextPick;
}

function getRecentPicks() {
	var currentPick = getPickNumber(),
		url = 'recent-picks/';

	var data = {
		'current_pick': currentPick
	};

	$.getJSON(url, data, function(response) {
		if(response.last_pick_team) {
			$('.last-pick').append(response.last_pick_team, " - ", response.last_pick_player);
		} else {
			$('.last-pick').append("<p>No previous pick</p>");
		} if(response.next_pick_team) {
			$('.next-pick').append(response.next_pick_team, " - Round ", response.next_pick_round, ", Pick ", response.next_pick_pick);
			nextPick = response.next_pick_number;
		} else {
			$('.next-pick').append("<p>No next pick</p>");
		}

		$('.on-the-clock-pick').append(response.current_pick_team, " - Round ", response.current_pick_round, ", Pick ", response.current_pick_pick);
	})
}

function showAll() {
	$('.all-players').removeClass('hidden');
	$('.all-list').addClass('unclickable');
}

function showQBs() {
	$('.qb-players').removeClass('hidden');
	$('.qb-list').addClass('unclickable');
}

function showRBs() {
	$('.rb-players').removeClass('hidden');
	$('.rb-list').addClass('unclickable');
}

function showWRs() {
	$('.wr-players').removeClass('hidden');
	$('.wr-list').addClass('unclickable');
}

function showTEs() {
	$('.te-players').removeClass('hidden');
	$('.te-list').addClass('unclickable');
}

function showDEFs() {
	$('.def-players').removeClass('hidden');
	$('.def-list').addClass('unclickable');
}

function showKs() {
	$('.k-players').removeClass('hidden');
	$('.k-list').addClass('unclickable');
}

function showRoster(e) {
	e.preventDefault();
	$('.roster-board').empty();
	var $team = $('.team-select-dropdown').find('option:selected')[0].id;

	var rosterArray = getRosterArray(),
		url = 'rosters/',
		payload = {
			'roster': rosterArray,
			'team': $team
		};

	$.getJSON(url, payload, function(response) {
		var draftedPlayers = response.roster;

		for(var i = 0; i < rosterArray.length; i++) {
			if(draftedPlayers[i]) {
				$('.roster-board').append(rosterArray[i] + " - " + draftedPlayers[i] + '<br>');
			} else {
				$('.roster-board').append(rosterArray[i] + " - Empty <br>");
			}
		}
	});
}

function getRosterArray() {
	var string = localStorage.getItem('rosterArray'),
		array = string.split(',');
	return array;
}
