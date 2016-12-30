// Functxon to set the player positions into HTML
function setPlayerPosition(player_value, player_pos) {
    var x = player_pos[0];
    var y = player_pos[1];

    document.getElementById("maze").getElementsByTagName("tr")[y]
        .getElementsByTagName("td")[x].setAttribute("id", player_value);
}

// Get the player position
$.getJSON('/maze', function(data) {
    var player_1 = data["players"][0];
    var player_2 = data["players"][1];
    var player_3 = data["players"][2];
    var player_4 = data["players"][3];

    setPlayerPosition("player1", player_1);
    setPlayerPosition("player2", player_2);
    setPlayerPosition("player3", player_3);
    setPlayerPosition("player4", player_4);

    // var maze = data["maze"];

    // for (var y = maze.length - 1; y >= 0; y--) {
    //     for (var x = maze[y].length - 1; x >= 0; x--) {
    //         if (maze[y][x] == 0) {
    //             setPlayerPosition("showmaze", [x, y]);
    //         };
    //     };
    // };
})