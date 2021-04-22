# this file stores the functions for getting AI input at each game state


""" This function returns the distance between the given head and the closest wall (grid border or body) to the north
    Inputs: x,y coordinate of a snakes head
"""
def _dist_north(x, y, p_bodies, grid_size, snake_speed):
    dist = 0
    for grid_y in range(y, grid_size, snake_speed):
        if p_bodies[x, grid_y]: break
        else: dist += 1
    return dist


def _dist_south(x, y, p_bodies, snake_speed):
    dist = 0
    for grid_y in range(y, -1, -snake_speed):
        if p_bodies[x, grid_y]: break
        else: dist += 1
    return dist


def _dist_east(x, y, p_bodies, grid_size, snake_speed):
    dist = 0
    for grid_x in range(x, grid_size, snake_speed):
        if p_bodies[grid_x, y]: break
        else: dist += 1
    return dist


def _dist_west(x, y, p_bodies, snake_speed):
    dist = 0
    for grid_x in range(x, -1, -snake_speed):
        if p_bodies[grid_x, y]: break
        else: dist += 1
    return dist


"""
calculate distance information
information is returned in 2 lists
red's list(first list returned) [self_north, self_south, self_east, self_west, blue_min_dist]
blue's list(second list returned) [self_north, self_south, self_east, self_west, red_min_dist]
red gets blue's min dist to be used for "aggression" and vis versa for blue
"""
def dist_totals(r_cord, b_cord, r_aim, b_aim, p_bodies, grid_size, snake_speed):

    r_dists = []
    b_dists = []

    # get distances for all 4 directions of each snake
    r_north = _dist_north(r_cord.x, r_cord.y, p_bodies, grid_size, snake_speed)
    r_south = _dist_south(r_cord.x, r_cord.y, p_bodies, snake_speed)
    r_east = _dist_east(r_cord.x, r_cord.y, p_bodies, grid_size, snake_speed)
    r_west = _dist_west(r_cord.x, r_cord.y, p_bodies, snake_speed)

    b_north = _dist_north(b_cord.x, b_cord.y, p_bodies, grid_size, snake_speed)
    b_south = _dist_south(b_cord.x, b_cord.y, p_bodies, snake_speed)
    b_east = _dist_east(b_cord.x, b_cord.y, p_bodies, grid_size, snake_speed)
    b_west = _dist_west(b_cord.x, b_cord.y, p_bodies, snake_speed)

    # append the distance to the b/r's dist list only if not facing opposite direction
    if r_aim.y >= 0: r_dists.append(r_north)
    if r_aim.y <= 0: r_dists.append(r_south)
    if r_aim.x >= 0: r_dists.append(r_east)
    if r_aim.x <= 0: r_dists.append(r_west)

    if b_aim.y >= 0: b_dists.append(b_north)
    if b_aim.y <= 0: b_dists.append(b_south)
    if b_aim.x >= 0: b_dists.append(b_east)
    if b_aim.x <= 0: b_dists.append(b_west)

    # for each snake, return their distances from walls, as well as opponents min distance
    return [min(3, r_north), min(3, r_south), min(3, r_east), min(3, r_west), min(3, min(b_dists))],\
           [min(3, b_north), min(3, b_south), min(3, b_east), min(3, b_west), min(3, min(r_dists))]