function update_tile(idx, val) { 
	var tile = document.getElementById(idx);
	if (val != "None") {
		tile.innerHTML = val;
		tile.disabled = true;
		if (val == "X") {
			tile.className = "board x";
		} else if (val == "O") {
			tile.className = "board o";
		}
	} else {
		tile.innerHTML = "";
		tile.disabled = false;
		tile.className = "board"
	}
}

function update_board(game_over, message) {
	var reset = document.getElementById("reset");
	var msg = document.getElementById("msg");
	msg.innerHTML = message;
	if (game_over == "True") {
		reset.disabled = false;
		
		for (i=0; i<9; i++) {
			tile = document.getElementById('' + i);
			tile.disabled = true;
		}
		
	} else {
		reset.disabled = true;
	}
}

/*
function update_score(can_player_join, players) {
	
	var scores = document.getElementById("scores");
	scores.style.display = "none";
	
	if (can_player_join == "False") {

		scores.style.display = "table";
	
		var names = document.getElementById("names");
		var wins = document.getElementById("wins");
		
		names.innerHTML = "<td>" + players[0].name + "</td><td>" + players[1].name + "</td>";
		wins.innerHTML = "<td>" + players[0].wins + "</td><td>" + players[1].wins + "</td>";		
		
	}
	
}
*/