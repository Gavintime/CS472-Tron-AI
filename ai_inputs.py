# this file stores the functions for getting AI input at each game state

from tron import SNAKE_SPEED, GRID_SIZE

""" This function returns the distance between the given head and the closest wall (grid border or body) to the north
    Inputs: x,y coordinate of a snakes head
"""
def dist_north(x, y, p_bodies):
    dist = 0
    for grid_y in range(y, GRID_SIZE, SNAKE_SPEED):
        if p_bodies[x, grid_y]: break
        else: dist += 1
    return dist


def dist_south(x, y, p_bodies):
    dist = 0
    for grid_y in range(y, -1, -SNAKE_SPEED):
        if p_bodies[x, grid_y]: break
        else: dist += 1
    return dist


def dist_east(x, y, p_bodies):
    dist = 0
    for grid_x in range(x, GRID_SIZE, SNAKE_SPEED):
        if p_bodies[grid_x, y]: break
        else: dist += 1
    return dist


def dist_west(x, y, p_bodies):
    dist = 0
    for grid_x in range(x, -1, -SNAKE_SPEED):
        if p_bodies[grid_x, y]: break
        else: dist += 1
    return dist


