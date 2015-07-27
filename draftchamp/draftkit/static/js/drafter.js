var $teamID,
	$playerID

$(function() {
	$('form[name=big-board]').submit(draftSelectedPlayer); 

	//Set pick and round number storage if we haven't yet
	if(!localStorage.getItem('pickNumber') && !localStorage.getItem('roundNumber')) {
		localStorage['pickNumber'] = 1;
		localStorage['roundNumber'] = 1;
	}

});

function draftSelectedPlayer(e) {
	e.preventDefault();

	var $form = $(e.target);
	$playerID = $form.find('select option:selected')[0].id;
	$teamID = 1;

	var roundNumber = getRoundNumber();
	var pickNumber = getPickNumber();

	var url = 'selection/'+roundNumber+'/'+pickNumber+'/';

	var data = {
		'player': $playerID,
		'team': $teamID
	}

	$.getJSON(url, data, function(response) {
		if(response.status == 1) {
			alert("It worked!");
			//Increment pick number (and round, if applicable)
			incrementPick();
			window.top.location.reload();
		} else {
			console.log("It didn't work :/");
		}
	});
}

function getPickNumber() {
	return parseInt(localStorage.getItem('pickNumber'), 10);
}

function getRoundNumber() {
	return parseInt(localStorage.getItem('roundNumber'), 10);
}

function incrementPick() {
	var pick = getPickNumber();
	console.log()
	//If pick number is not last pick of round, increment. If it is last pick of round, drop pick to 1 and increment round
	if(pick < 3) {
		pick++;
		localStorage['pickNumber'] = pick;
	} else {
		localStorage['pickNumber'] = 1;
		var round = getRoundNumber();
		round++;
		localStorage['roundNumber'] = round;
	}
}

//Create method to get draft specs and save as localstorage