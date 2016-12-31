from django.shortcuts import render

from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def maze(request):
    f = open("maze.json", "r")
    maze = json.load(f)
    f.close()
    if request.method == "POST":
        # Get data
        player_no = int(request.POST["player_no"])-1
        moves = json.loads(request.POST["moves"])

        height = len(maze["maze"])
        width = len(maze["maze"][0])

        """
        0 - up
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
            nx = player_pos[0] + dx[moves[i]]
            ny = player_pos[1] + dy[moves[i]]

            # Check that moves are within grid
            if (nx >= 0 and nx < width and ny >= 0 and ny < height and
                    maze["maze"][ny][nx] != 0):
                player_pos[0] = nx
                player_pos[1] = ny
            else:
                moves[i] *= -1
        maze["players"][player_no] = player_pos
        maze["previous_moves"] = [player_no+1] + moves

        # Rewrite json file
        f = open("maze.json", "w")
        json.dump(maze, f)
        f.close()

        return HttpResponse('')
    else:
        # del maze["maze"]
        return JsonResponse(maze)