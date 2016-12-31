from django.shortcuts import render

from django.http import HttpResponse

import json

def join(request):
	response = ""
	f = open("players.json", "r+")
	data = json.load(f)

	try:
		new_player = data["players"].index(False)

		data["players"][new_player] = True
		response = new_player+1

		f.truncate(0)
		f.seek(0, 0)
		json.dump(data, f)
	except ValueError:
		response = "max"

	f.close()

	return HttpResponse(response)

def leave(request, player_no):
	f = open("players.json", "r+")
	data = json.load(f)

	data["players"][int(player_no)-1] = False

	f.truncate(0)
	f.seek(0, 0)
	json.dump(data, f)

	f.close()

	return HttpResponse("")