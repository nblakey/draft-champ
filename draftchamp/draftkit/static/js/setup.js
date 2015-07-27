$(function() {
	$('form[name=number-of-teams]').submit(setNumberOfTeams);

	var numberOfTeams,
		teamsToCreate;
});

function setNumberOfTeams(e) {
	e.preventDefault();

	var $dropDown = $(e.target);
	numberOfTeams = parseInt($dropDown.find('select option:selected')[0].value, 10);
	teamsToCreate = [];

	intakeTeamInfo();
}

function intakeTeamInfo() {
	$('form[name=create-team]').submit(createTeam);

	$('.number-of-teams').addClass("hidden");
	$('.create-team').removeClass("hidden");
}

function createTeam(e) {
	e.preventDefault();

	if(teamsToCreate.length < 1) {
		var	teamName = document.getElementById('id_team_name').value,
			ownerFirst = document.getElementById('id_owner_first_name').value,
			ownerLast = document.getElementById('id_owner_last_name').value,
			ownerEmail = document.getElementById('id_owner_email').value,
			ownerOrder = document.getElementById('id_owner_draft_position').value,
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
	} if(teamsToCreate.length == 1) {
		console.log("Creating teams!");

		var teamsJSON = JSON.stringify(teamsToCreate);

		var payload = {
			'teams': teamsJSON
		}

		$.getJSON('create-teams/', payload, function(response) {
			console.log(response.status);
		});
		// window.location.href = "/draftkit/big-board/";
	}

}

/* To do:
- Create picks order based on draft position, no trades for now
*/