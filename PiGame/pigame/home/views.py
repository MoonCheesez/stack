from django.shortcuts import render

import json

# Create your views here.
def home(request):
    # Read the last moves
    f = open("maze.json", "r")
    data = json.load(f)
    f.close()

    context = {
        "data": data["previous_moves"],
        "length": range(len(data["maze"][0])),
        "breadth": range(len(data["maze"]))
    }

    return render(request, "home/home.html", context)