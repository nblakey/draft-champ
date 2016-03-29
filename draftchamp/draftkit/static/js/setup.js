$(function() {
	$('form[name=number-of-teams]').submit(setNumberOfTeams);

	var numberOfTeams,
		rosterSize,
		teamsToCreate;

	if(localStorage.getItem('overallPickNumber')) {
		localStorage.removeItem('overallPickNumber');
	}
});

function setNumberOfTeams(e) {
	e.preventDefault();

	var $dropDown = $(e.target);
	numberOfTeams = parseInt($dropDown.find('select option:selected')[0].value, 10);
	teamsToCreate = [];

	intakeRosterInfo();
}

function intakeRosterInfo() {
	$('form[name=roster-setup]').submit(setRosterInfo);

	$('.number-of-teams').addClass("hidden");
	$('.roster-setup').removeClass("hidden");
}

function setRosterInfo(e) {
	e.preventDefault();

	var qbs = parseInt(document.getElementById('id_qbs').value, 10),
		rbs = parseInt(document.getElementById('id_rbs').value, 10),
		wrs = parseInt(document.getElementById('id_wrs').value, 10),
		tes = parseInt(document.getElementById('id_tes').value, 10),
		defs = parseInt(document.getElementById('id_defs').value, 10),
		ks = parseInt(document.getElementById('id_ks').value, 10),
		rbwrs = parseInt(document.getElementById('id_rbwrs').value, 10),
		flexs = parseInt(document.getElementById('id_flexs').value, 10),
		ops = parseInt(document.getElementById('id_ops').value, 10),
		bes = parseInt(document.getElementById('id_bes').value, 10);

	rosterSize = qbs + rbs + wrs + tes + defs+ ks + rbwrs + flexs + ops + bes;

	var rosterArray = [];

	for(var i = 0; i < qbs; i++) {
		rosterArray.push('QB');
	} for(var i = 0; i < rbs; i++) {
		rosterArray.push('RB');
	} for(var i = 0; i < wrs; i++) {
		rosterArray.push('WR');
	} for(var i = 0; i < tes; i++) {
		rosterArray.push('TE');
	} for(var i = 0; i < defs; i++) {
		rosterArray.push('DEF');
	} for(var i = 0; i < ks; i++) {
		rosterArray.push('K');
	} for(var i = 0; i < rbwrs; i++) {
		rosterArray.push('RB/WR');
	} for(var i = 0; i < flexs; i++) {
		rosterArray.push('FLEX');
	} for(var i = 0; i < ops; i++) {
		rosterArray.push('OP');
	} for(var i = 0; i < bes; i++) {
		rosterArray.push('BE');
	}

	localStorage['rosterArray'] = rosterArray;

	intakeTeamInfo();
}

function intakeTeamInfo() {
	$('form[name=create-team]').submit(createTeam);

	$('.roster-setup').addClass("hidden");
	$('.create-team').removeClass("hidden");
}

function createTeam(e) {
	e.preventDefault();

	if(teamsToCreate.length < numberOfTeams) {
		var	teamName = document.getElementById('id_team_name').value,
			ownerFirst = document.getElementById('id_owner_first_name').value,
			ownerLast = document.getElementById('id_owner_last_name').value,
			ownerEmail = document.getElementById('id_owner_email').value,
			ownerOrder = parseInt(document.getElementById('id_owner_draft_position').value, 10),
			inArray = false,
			formCompleted = true;
			draftOrderValid = true;

		if(teamName && ownerFirst && ownerLast && ownerEmail && ownerOrder) {
			if(teamsToCreate.length != 0) {
				for(var i = 0; i < teamsToCreate.length; i++) {
					if(teamsToCreate[i].ownerOrder == ownerOrder) {
						inArray = true;
						alert("That draft position is already filled!");
						break;
					}
				}
			} if(isNaN(ownerOrder)) {
				draftOrderValid = false;
				alert("Draft order must be a number!");
			} else if(ownerOrder < 1 || ownerOrder > numberOfTeams) {
				draftOrderValid = false;
				alert("The draft order must be between 1 and " + numberOfTeams + "!");
			}
		} else {
			formCompleted = false;
			alert("The form was not completed!");
		}

		if(formCompleted && !inArray && draftOrderValid) {
			var newTeam = {
				'teamName': teamName,
				'ownerFirst': ownerFirst,
				'ownerLast': ownerLast,
				'ownerEmail': ownerEmail,
				'ownerOrder': ownerOrder
			};

			teamsToCreate.push(newTeam);

			$('.teams-list').append(ownerFirst, " ", ownerLast, " - ", teamName, "<br>");
			$('.teams-to-add').removeClass("hidden");
			document.getElementById('create-team-form').reset();
		}
	} if(teamsToCreate.length == numberOfTeams) {

		teamsToCreate.sort(function(a, b) {
			if(a.ownerOrder > b.ownerOrder) {
				return 1;
			} else if(a.ownerOrder < b.ownerOrder) {
				return -1;
			}
			return 0;
		});
		var teamsJSON = JSON.stringify(teamsToCreate),
			createPlayersTrigger = localStorage.getItem('createPlayersTrigger') || 'False';

		var payload = {
			'teams': teamsJSON,
			'rosterSize': rosterSize,
			'trigger': createPlayersTrigger
		}

		$.getJSON('create-teams/', payload, function(response) {
			if(response.status == 1) {
				window.location.href = "/draftkit/keepers/";
			}
		});
	}

}