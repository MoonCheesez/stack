import json
from generate_maze import *

length = 32
breadth = 32
# Generate maze
m = generate_maze(length, breadth, (0, 0))
player_pos = [(0, 0), (length-1, 0), (length-1, breadth-1), (0, breadth-1)]

# Write to file
f = open("maze.json", "w")
json.dump({"maze": m, "players": player_pos, "previous_moves": []}, f)
f.close()