# this file stores the functions for getting AI input at each game state

# effectively how far in each direction the snake can see a wall
FORESIGHT = 3

""" This function returns the distance between the given head and the closest wall (grid border or body) to the north
    Inputs: x,y coordinate of a snakes head
"""
def _dist_north(x, y, p_bodies, grid_size, snake_speed):
    dist = FORESIGHT
    for grid_y in range(y+snake_speed, grid_size, snake_speed):
        if p_bodies[x, grid_y] or dist == 0: break
        else: dist -= 1
    return dist


def _dist_south(x, y, p_bodies, snake_speed):
    dist = FORESIGHT
    for grid_y in range(y-snake_speed, -1, -snake_speed):
        if p_bodies[x, grid_y] or dist == 0: break
        else: dist -= 1
    return dist


def _dist_east(x, y, p_bodies, grid_size, snake_speed):
    dist = FORESIGHT
    for grid_x in range(x+snake_speed, grid_size, snake_speed):
        if p_bodies[grid_x, y] or dist == 0: break
        else: dist -= 1
    return dist


def _dist_west(x, y, p_bodies, snake_speed):
    dist = FORESIGHT
    for grid_x in range(x-snake_speed, -1, -snake_speed):
        if p_bodies[grid_x, y] or dist == 0: break
        else: dist -= 1
    return dist


"""
calculate distance information
information is returned in 2 lists
red's list(first list returned) [self_north, self_south, self_east, self_west, blue_min_dist]
blue's list(second list returned) [self_north, self_south, self_east, self_west, red_min_dist]
red gets blue's min dist to be used for "aggression" and vis versa for blue
"""
def dist_totals(r_cord, b_cord, p_bodies, grid_size, snake_speed):

    # get distances for all 4 directions of each snake
    r_north = _dist_north(r_cord.x, r_cord.y, p_bodies, grid_size, snake_speed)
    r_south = _dist_south(r_cord.x, r_cord.y, p_bodies, snake_speed)
    r_east = _dist_east(r_cord.x, r_cord.y, p_bodies, grid_size, snake_speed)
    r_west = _dist_west(r_cord.x, r_cord.y, p_bodies, snake_speed)

    b_north = _dist_north(b_cord.x, b_cord.y, p_bodies, grid_size, snake_speed)
    b_south = _dist_south(b_cord.x, b_cord.y, p_bodies, snake_speed)
    b_east = _dist_east(b_cord.x, b_cord.y, p_bodies, grid_size, snake_speed)
    b_west = _dist_west(b_cord.x, b_cord.y, p_bodies, snake_speed)


    # for each snake, return their distances from 4 cardinal walls,
    # coordinates for itself and opponent
    # distances from each other, and a var stating if red or blue
    return [r_north / FORESIGHT,
            r_south / FORESIGHT,
            r_east / FORESIGHT,
            r_west / FORESIGHT,
            r_cord.x / grid_size,
            r_cord.y / grid_size,
            b_cord.x / grid_size,
            b_cord.y / grid_size],\
           [b_north / FORESIGHT,
            b_south / FORESIGHT,
            b_east / FORESIGHT,
            b_west / FORESIGHT,
            b_cord.x / grid_size,
            b_cord.y / grid_size,
            r_cord.x / grid_size,
            r_cord.y / grid_size]
