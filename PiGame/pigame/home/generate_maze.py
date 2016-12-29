import random

def validate(pos, maze):
    x = pos[0]
    y = pos[1]
    mx = maze[0]
    my = maze[1]

    return (x >= 0 and x < mx) and (y >= 0 and y < my)

def generate_maze(length, breadth, start_pos):
    """Generates a maze as a 2D list
    0 represents a wall in the maze while 1 represents an empty space
    
    length - horizontal length of maze
    breadth - vertical length of maze
    start_pos - tuple of the starting position, (length, breadth)
    """

    # Fill maze with zeros
    maze = [[0 for x in range(length)] for y in range(breadth)]
    # Previously visited positions
    stack = [start_pos]

    # Directions
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    while stack:
        (current_x, current_y) = stack[-1]
        maze[current_y][current_x] = 1

        neighbours = []
        for i in range(4):
            neighbour_x = current_x + dx[i]
            neighbour_y = current_y + dy[i]

            # Ensure that the neighbour's position is valid
            if validate((neighbour_x, neighbour_y), (length, breadth)):
                if maze[neighbour_y][neighbour_x] == 0:
                    ctr = 0
                    for j in range(4):
                        ex = neighbour_x + dx[j]
                        ey = neighbour_y + dy[j]

                        if (validate((ex, ey), (length, breadth)) and
                                maze[ey][ex] == 1):
                            ctr += 1

                    if ctr == 1:
                        neighbours.append(i)

        if neighbours:
            ir = neighbours[random.randint(0, len(neighbours) - 1)]
            current_x += dx[ir]
            current_y += dy[ir]
            
            stack.append((current_x, current_y))
        else:
            stack.pop()

    return maze

m = generate_maze(32, 32, (0, 0))
for i in m: print("".join([str(x) for x in i]))