from django.shortcuts import render

import json
import random
from quotes import quotes

# Create your views here.
def home(request):
    # Read the last moves
    f = open("maze.json", "r")
    data = json.load(f)
    f.close()

    # Read the number of players
    f = open("players.json", "r")
    players_left = json.load(f)["players"].count(False)
    f.close()

    quote = random.choice(quotes)

    context = {
        "data": data["previous_moves"],
        "length": range(len(data["maze"][0])),
        "breadth": range(len(data["maze"])),
        "players_left": players_left,
        "quote": quote,
    }

    return render(request, "home/home.html", context)