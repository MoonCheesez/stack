// Functxon to set the player positions into HTML
function setPlayerPosition(player_value, player_pos) {
    var x = player_pos[0];
    var y = player_pos[1];

    document.getElementById("maze").getElementsByTagName("tr")[y]
        .getElementsByTagName("td")[x].setAttribute("id", player_value);
}

function movePlayer(player_value, from, to) {
    setPlayerPosition("", from);
    setPlayerPosition(player_value, to);
}

function getNextLocation(move, currentPos) {
    // Moves the player and returns that location
    var dx = [0, -1, 1, 0];
    var dy = [-1, 0, 0, 1];

    var nx = currentPos[0] + dx[move];
    var ny = currentPos[1] + dy[move];

    if (nx >= 0 && ny >= 0) {
        return [nx, ny];
    } else {
        return currentPos;
    }
}

function displayString(value) {
    setTimeout(function() {
        document.getElementById("current_move").innerHTML = "";    
    }, 500);
    document.getElementById("current_move").innerHTML = value;
}

var startup = true;

var playerPositions = [null, null, null, null];
var playerValues = ["player1", "player2", "player3", "player4"];

var moves = [];
var moveTypes = ["move_up", "move_left", "move_right", "move_down"];
var playerMoving;

var data;
$(document).ready(function() {

    // Setup
    $.getJSON("/maze", function(d) {
        playerMoving = d["previous_moves"][0]
        // Draw players
        for (var i=0; i<4; i++) {
            var newPosition = d["players"][i];
            setPlayerPosition(playerValues[i], newPosition);
            playerPositions[i] = newPosition;
        };


        // Show maze
        var maze = d["maze"];
        for (var y = maze.length - 1; y >= 0; y--) {
            for (var x = maze[y].length - 1; x >= 0; x--) {
                if (maze[y][x] == 0) {
                    setPlayerPosition("showmaze", [x, y]);
                };
            };
        };

    });

    window.setInterval(function() {
        $.getJSON("/maze", function(d) {
            data = d;
        });

        if (startup) {
            moves = data["previous_moves"];
            
            if (moves.length > 0 && moves[0] != playerMoving) {
                moves = data["previous_moves"].slice(1, data["previous_moves"].length);
                playerMoving = data["previous_moves"][0];
                startup = false;
            }

        } else if (moves.length > 0) {
            move = moves.shift();

            var currentPosition = playerPositions[playerMoving-1];
            var nextPosition = getNextLocation(move, currentPosition);

            movePlayer(playerValues[playerMoving-1],
                currentPosition, nextPosition);
            
            // Set new location
            playerPositions[playerMoving-1] = nextPosition;

            displayString(moveTypes[Math.abs(move)]);
        } else if (playerMoving != data["previous_moves"][0]) {
            moves = data["previous_moves"].slice(1, data["previous_moves"].length);
            playerMoving = data["previous_moves"][0];
        } else {
            displayString("");
        }
    }, 1000);
});