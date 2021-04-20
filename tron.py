"""Tron, a classic arcade game."""
import time
import turtle
import numpy as np
from freegames import vector
from ai_inputs import *
from enum import Enum


# when disabled, no turtle graphics are drawn, should be used when training AI
GRAPHICS_ENABLE = True
# toggles debugging printout (when someone turns, coordinate printout)
DEBUG_TEXT = True
# End Game printout toggle (ascii grid, winner)
END_TEXT = True
# controls if ai is enabled/ human controled
# TODO: controls on who to set for each AI
AI_RED = False
AI_BLUE = False


# speed as in distance traveled after each "frame"
SNAKE_SPEED = 4
# Number of milliseconds between a game state/frame advance
# effectively inverse speed of how fast game advances, lower numbers give faster "frame rate"
# speed of game is also impacted by turtle graphics and if dist funcs are calculated
DELAY = 20
# this needs to be divisible by SNAKE_SPEED for grids to align properly
GRID_SIZE = 400
WINDOW_SIZE = GRID_SIZE + 2


# starting location of the snakes
p1xy = vector(int(GRID_SIZE * .25), int(GRID_SIZE * .5))
p2xy = vector(int(GRID_SIZE * .75), int(GRID_SIZE * .5))
# starting direction of the snakes
p1aim = vector(SNAKE_SPEED, 0)
p2aim = vector(-SNAKE_SPEED, 0)


# numpy 2d GRID_TIMES x GRID_TIMES array, prefilled with 0s
# when a body piece is added its location is set to 1
# the boarder is set to 3(true) and is also a "body"
p_bodies = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
# add grid borders to p_bodies
for col in range(len(p_bodies)):
    for row in range(len(p_bodies[col])):
        if row == 0 or row == GRID_SIZE-4 or col == 0 or col == GRID_SIZE-4:
            p_bodies[col][row] = True


# enum status of the game
class Game_State(Enum):
    ongoing = 1
    red_won = 2
    blue_won = 3
    tie = 4


def draw_square(t, x, y):
    t.penup()
    t.setpos(x+1, y+1)
    t.begin_fill()
    t.setheading(0)
    t.pendown()
    t.forward(SNAKE_SPEED-1)
    t.setheading(270)
    t.forward(SNAKE_SPEED-1)
    t.setheading(180)
    t.forward(SNAKE_SPEED-1)
    t.setheading(90)
    t.forward(SNAKE_SPEED-1)
    t.end_fill()
    t.penup()


def print_grid(grid):
    for y in range(GRID_SIZE-4, -1, -4):
        for x in range(0, GRID_SIZE, 4):
            if grid[x,y]: print('0', end='')
            else: print('.', end='')
        print()

    print(p1xy, p2xy)


""" GAME INPUT FUNCTIONS
    Updates the direction of the red snake
    Input: Vector of direction to move p1
"""
def movep1(x, y):
    # ignore moves that go reverse
    if x == p1aim.x or y == p1aim.y: return
    p1aim.x = x
    p1aim.y = y
    if DEBUG_TEXT: print("Red TURN!")


def movep2(x, y):
    # ignore moves that go reverse
    if x == p2aim.x or y == p2aim.y: return
    p2aim.x = x
    p2aim.y = y
    if DEBUG_TEXT: print("Blue TURN!")


# returns Game_State enum depending who won
def draw(screen, t_red, t_blue, t_draw):

    # draw the head of each snake
    if GRAPHICS_ENABLE:
        t_draw.color("red")
        draw_square(t_draw, p1xy.x, p1xy.y)
        t_draw.color("blue")
        draw_square(t_draw, p2xy.x, p2xy.y)

    # increment the snake heads in the direction of their current aim
    p1xy.move(p1aim)
    p1head = p1xy.copy()
    p2xy.move(p2aim)
    p2head = p2xy.copy()

    # move the visual heads of each snake
    if GRAPHICS_ENABLE:
        t_red.setpos(p1xy.x, p1xy.y)
        t_blue.setpos(p2xy.x, p2xy.y)

    # alive flags
    red_alive = True
    blue_alive = True

    # Check if Red died
    if p_bodies[p1head.x, p1head.y]:
        red_alive = False
    # Check if Blue Died
    if p_bodies[p2head.x, p2head.y]:
        blue_alive = False

    # end game if either player is dead or hit each other
    if p1head == p2head or (not red_alive and not blue_alive):
        return Game_State.tie
    elif not red_alive:
        return Game_State.blue_won
    elif not blue_alive:
        return Game_State.red_won

    # print debug info
    if DEBUG_TEXT: print(dist_totals(p1head, p2head, p1aim, p2aim, p_bodies))

    # Add the current players heads to the body array
    p_bodies[p1head.x, p1head.y] = True
    p_bodies[p2head.x, p2head.y] = True

    # update screen and goto next game state
    if GRAPHICS_ENABLE:
        screen.update()

    return Game_State.ongoing


def main():

    screen = None
    t_red = None
    t_blue = None
    t_draw = None

    if GRAPHICS_ENABLE:

        # setup screen
        screen = turtle.Screen()
        screen.setup(WINDOW_SIZE, WINDOW_SIZE)
        screen.screensize(GRID_SIZE, GRID_SIZE, "black")     # sets drawable area of the turtle

        # disable turtle drawing animation, screen.update() will be used to update screen
        screen.tracer(False)

        # setup turtles to draw with or display
        turtle.mode("world")
        turtle.setworldcoordinates(0, 0, GRID_SIZE, GRID_SIZE)

        # visual head of red
        t_red = turtle.Turtle()
        t_red.penup()
        t_red.color("#FF6600")
        t_red.shape("square")
        t_red.shapesize(.4)

        # visual head of blue
        t_blue = turtle.Turtle()
        t_blue.penup()
        t_blue.color("#00FFFF")
        t_blue.shape("square")
        t_blue.shapesize(.4)

        # the turtle that actually draws
        t_draw = turtle.Turtle()
        t_draw.hideturtle()
        t_draw.penup()

        # draw playable area border
        t_draw.pensize(5)
        t_draw.color("white")
        t_draw.setpos(0,0)
        t_draw.setheading(0)
        t_draw.pendown()
        t_draw.forward(GRID_SIZE)
        t_draw.setheading(90)
        t_draw.forward(GRID_SIZE-4)
        t_draw.setheading(180)
        t_draw.forward(GRID_SIZE)
        t_draw.setheading(270)
        t_draw.forward(GRID_SIZE-4)
        t_draw.pensize(1)

    # if graphics disabled
    else:
        # when not using graphics, create tiny screen
        screen = turtle.Screen()
        screen.setup(140, 50)

    # set focus to screen to get inputs if at least one human player
    if not AI_RED or not AI_BLUE: screen.listen()

    # Red Inputs, standard wsad controls for North South West East
    if not AI_RED:
        screen.onkey(lambda: movep1(0, SNAKE_SPEED), 'w')
        screen.onkey(lambda: movep1(0, -SNAKE_SPEED), 's')
        screen.onkey(lambda: movep1(-SNAKE_SPEED, 0), 'a')
        screen.onkey(lambda: movep1(SNAKE_SPEED, 0), 'd')

    # Blue Inputs, same as reds inputs but with ikjl
    if not AI_BLUE:
        screen.onkey(lambda: movep2(0, SNAKE_SPEED), 'i')
        screen.onkey(lambda: movep2(0, -SNAKE_SPEED), 'k')
        screen.onkey(lambda: movep2(-SNAKE_SPEED, 0), 'j')
        screen.onkey(lambda: movep2(SNAKE_SPEED, 0), 'l')

    # begin game state/draw loop
    state = Game_State.ongoing
    while state == Game_State.ongoing:
        state = draw(screen, t_red, t_blue, t_draw)
        time.sleep(DELAY * 0.001)

    # run code here after game ends
    print(state)

    # disable user inputs after game ends
    if not AI_RED:
        screen.onkey(None, 'w')
        screen.onkey(None, 's')
        screen.onkey(None, 'a')
        screen.onkey(None, 'd')
    if not AI_BLUE:
        screen.onkey(None, 'i')
        screen.onkey(None, 'k')
        screen.onkey(None, 'j')
        screen.onkey(None, 'l')

    # keep window open after game finishes only if graphics enabled (interactive)
    if GRAPHICS_ENABLE: turtle.done()


# this just tells python to run the main method
if __name__ == "__main__": main()