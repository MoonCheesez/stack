from django.shortcuts import render

from django.http import JsonResponse

import json

# Create your views here.
def maze(request):
    f = open("maze.json", "r")
    maze = json.load(f)
    f.close()
    if request.method == "POST":
        # Get data
        player_no = request.POST["player_no"]-1
        moves = json.loads(request.POST["moves"])


        """
        0 - forward
        1 - left
        2 - right
        3 - down
        """
        player_pos = maze["players"][player_no]
        # Move the player
        dx = [0, -1, 1, 0]
        dy = [-1, 0, 0, 1]

        previous_positions = []

        for i in range(len(moves)):
            # Validate position
            nx = player_pos + dx[moves[i]]
            ny = player_pos + dy[moves[i]]

            if maze[ny][nx] != 0:
                player_pos[0] += nx
                player_pos[1] += ny
            else:
                moves[i] *= -1
        maze["players"][player_no] = player_pos
        maze["previous_moves"] = moves

        # Rewrite json file
        f = open("maze.json", "w")
        json.dump(maze, f)
        f.close()

        return
    else:
        del maze["maze"]
        return JsonResponse(maze)