$(function() {
	$('form[name=trade-picks]').submit(tradePicks);

	document.getElementById('cancel-trades').onclick = function() {
		$('form[name=keeper-picks]').submit(keepPlayers);

		$('.picks-to-trade').addClass('hidden');
		$('.keeper-picks').removeClass('hidden');

		document.getElementById('cancel-keepers').onclick = function() {
			window.location.href = "/draftkit/big-board/";
		}
	}
});

function tradePicks(e) {
	e.preventDefault();
	var team1 = document.getElementById('id_team_1').value,
		team2 = document.getElementById('id_team_2').value,
		round1 = document.getElementById('id_round_1').value,
		round2 = document.getElementById('id_round_2').value;

	var payload = {
		'team1': team1,
		'team2': team2,
		'round1': round1,
		'round2': round2
	};

	$.getJSON('trade/', payload, function(response) {
		if(response.status == 1) {
			document.getElementById('picks-to-trade-form').reset();
		} else if(response.status == 2) {
			alert("Team 1 does not have a pick to trade in that round!");
		} else if(response.status == 3) {
			alert("Team 2 does not have a pick to trade in that round!");
		}
	});
}

function keepPlayers(e) {
	e.preventDefault();
	var team = document.getElementById('id_team').value,
		draft_round = document.getElementById('id_draft_round').value,
		player = document.getElementById('id_player').value;

	var payload = {
		'team': team,
		'draft_round': draft_round,
		'player': player
	};

	$.getJSON('keep/', payload, function(response) {
		if(response.status == 1) {
			document.getElementById('keeper-picks-form').reset();
		} else if(response.status == 2){
			alert("Team 1 does not have a draft pick in that round!");
		}
	});
}