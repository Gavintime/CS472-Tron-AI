"""
    Tron, classic arcade game.
"""
import threading
from turtle import Screen, Turtle, done, mode, setworldcoordinates
import numpy as np
from freegames import vector

SNAKE_SPEED = 4

# Number of milliseconds between a game state/frame advance
# effectively inverse speed of how fast game advances, lower numbers give faster "frame rate"
DELAY = 10

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
p_bodies = np.zeros((GRID_SIZE+1, GRID_SIZE+1), dtype=bool)
for col in range(len(p_bodies)):
    for row in range(len(p_bodies[col])):
        if row == 4 or row == GRID_SIZE-4 or col == 0 or col == GRID_SIZE-4:  # check this, graphically it is correct
            p_bodies[col][row] = 3


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
    for y in range(GRID_SIZE-4, 1, -4):
        for x in range(0, GRID_SIZE, 4):
            if grid[x,y]: print('0', end='')
            else: print('.', end='')
        print()


""" GAME INPUT FUNCTION
    Updates the direction of the red snake
    Input: Vector of direction to move p1
"""
def movep1(x, y):
    # ignore moves that go reverse
    if x == p1aim.x or y == p1aim.y: return
    p1aim.x = x
    p1aim.y = y


def movep2(x, y):
    # ignore moves that go reverse
    if x == p2aim.x or y == p2aim.y: return
    p2aim.x = x
    p2aim.y = y


""" Checks if the given snakes head is within the playable grid bounds (GRID_SIZExGRID_SIZE)
    Input: x,y coordinates of the given snakes head
    Output: True if the snakes head is within GRID_SIZE bounds, False otherwise
"""
def inside(head):
    # Return True if head inside screen.
    return 0 <= head.x < GRID_SIZE \
           and 0 <= head.y < GRID_SIZE


def draw(screen, t_red, t_blue, t_draw):

    # draw the head of each snake
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
    t_red.setpos(p1xy.x, p1xy.y)
    t_blue.setpos(p2xy.x, p2xy.y)



    # alive flags
    red_alive = True
    blue_alive = True

    # Check if Red died
    if not inside(p1head) or p_bodies[p1head.x, p1head.y]:
        red_alive = False

    # Check if Blue Died
    if not inside(p2head) or p_bodies[p2head.x, p2head.y]:
        blue_alive = False

    # end game if either player is dead or hit each other
    if p1head == p2head \
            or (not red_alive and not blue_alive):
        print("Tie!")
        print_grid(p_bodies)
        return

    elif not red_alive:
        print("Blue Wins!")
        print_grid(p_bodies)
        return

    elif not blue_alive:
        print("Red Wins!")
        print_grid(p_bodies)
        return

    # Add the current players heads to the body array
    p_bodies[p1head.x, p1head.y] = 1
    p_bodies[p2head.x, p2head.y] = 2

    # update screen and goto next game state
    screen.update()
    threading.Timer(DELAY * .001, draw, args=[screen, t_red, t_blue, t_draw]).start()


def main():

    # setup screen
    screen = Screen()
    screen.setup(WINDOW_SIZE, WINDOW_SIZE)
    screen.screensize(GRID_SIZE, GRID_SIZE, "black")     # sets drawable area of the turtle

    # disable turtle drawing animation, screen.update() will be used to update screen
    screen.tracer(False)

    # setup turtles to draw with or display
    mode("world")
    setworldcoordinates(0, 0, GRID_SIZE, GRID_SIZE)

    # visual head of red
    t_red = Turtle()
    t_red.penup()
    t_red.color("#FF6600")
    t_red.shape("square")
    t_red.shapesize(.4)

    # visual head of blue
    t_blue = Turtle()
    t_blue.penup()
    t_blue.color("#00FFFF")
    t_blue.shape("square")
    t_blue.shapesize(.4)

    # the turtle that actually draws
    t_draw = Turtle()
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
    t_draw.forward(GRID_SIZE)
    t_draw.setheading(180)
    t_draw.forward(GRID_SIZE)
    t_draw.setheading(270)
    t_draw.forward(GRID_SIZE)
    t_draw.pensize(1)


    # enable user input listening, this should be disabled once AI testing starts
    screen.listen()

    # Red Inputs, standard wsad controls for North South West East
    screen.onkey(lambda: movep1(0, SNAKE_SPEED), 'w')
    screen.onkey(lambda: movep1(0, -SNAKE_SPEED), 's')
    screen.onkey(lambda: movep1(-SNAKE_SPEED, 0), 'a')
    screen.onkey(lambda: movep1(SNAKE_SPEED, 0), 'd')

    # Blue Inputs, same as reds inputs but with ikjl (vim like)
    screen.onkey(lambda: movep2(0, SNAKE_SPEED), 'i')
    screen.onkey(lambda: movep2(0, -SNAKE_SPEED), 'k')
    screen.onkey(lambda: movep2(-SNAKE_SPEED, 0), 'j')
    screen.onkey(lambda: movep2(SNAKE_SPEED, 0), 'l')

    # begin game state/draw loop
    draw(screen, t_red, t_blue, t_draw)
    # keep window open after game finishes
    done()


# this just tells python to run the main method
if __name__ == "__main__": main()