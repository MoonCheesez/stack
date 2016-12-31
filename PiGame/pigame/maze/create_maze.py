import json
from generate_maze import *

length = 32
breadth = 32

sub_length = int(length/2)
sub_breadth = int(breadth/2)

# Player 1 maze
m1 = generate_maze(sub_length, sub_breadth, (0, 0), (sub_length-1, sub_breadth-1))
# Player 2 maze
m2 = generate_maze(sub_length, sub_breadth, (sub_length-1, 0), (sub_length-1, sub_breadth-1))
# Player 3 maze
m3 = generate_maze(sub_length, sub_breadth, (sub_length-1, sub_breadth-1), (sub_length-1, sub_breadth-1))
# Player 4 maze
m4 = generate_maze(sub_length, sub_breadth, (0, sub_breadth-1), (sub_length-1, sub_breadth-1))

# Combine mazes
m = m1
for y in range(sub_breadth):
	m[y].extend(m2[y])
	m3[y].extend(m4[y])
m.extend(m3)

# Generate maze
player_pos = [(0, 0), (length-1, 0), (length-1, breadth-1), (0, breadth-1)]

# Write to file
f = open("maze.json", "w")
json.dump({"maze": m, "players": player_pos, "previous_moves": []}, f)
f.close()