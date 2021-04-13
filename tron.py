"""
    Tron, classic arcade game.
"""
from turtle import *
from freegames import square, vector


SNAKE_SPEED = 4

# Number of milliseconds between a game state/frame advance
# effectively inverse speed of how fast game advances, lower numbers give faster "frame rate"
DELAY = 25

# this needs to be divisible by SNAKE_SPEED for grids to align properly
GRID_SIZE = 200
WINDOW_SIZE = GRID_SIZE * 2 + 8


"""
    p1xy: current xy location of head
    p1aim: current direction of head as a vector
    p1body: set of vectors of previous head locations, the body of the snake
"""
p1xy = vector(-100, 0)
p1aim = vector(SNAKE_SPEED, 0)

p2xy = vector(100, 0)
p2aim = vector(-SNAKE_SPEED, 0)

p_bodies = set()


"""
    GAME INPUT FUNCTION
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


"""
    Checks if the given snakes head is within the playable grid bounds (GRID_SIZExGRID_SIZE)
    Input: x,y coordinates of the given snakes head
    Output: True if the snakes head is within GRID_SIZE bounds, False otherwise
"""
def inside(head):
    # Return True if head inside screen.
    return -GRID_SIZE < head.x < GRID_SIZE \
           and -GRID_SIZE < head.y < GRID_SIZE


# Advance Each snake and draw the game, recursively calls itself till game ends
def draw():

    # increment red's head in the direction of its current aim
    p1xy.move(p1aim)
    p1head = p1xy.copy()

    p2xy.move(p2aim)
    p2head = p2xy.copy()

    # There is a tie if both snakes hit something at the same time or heads collide
    if (not inside(p1head) and not inside(p2head)) \
            or ((p1head in p_bodies)
            and (p2head in p_bodies)) \
            and p1head == p2head:

        print('Tie!')
        return

    # Blue wins if the red snake hits the grid bounds, or either of the bodies
    if not inside(p1head) or p1head in p_bodies:
        print('Player blue wins!')
        return

    # Red wins if the Blue snake ...
    if not inside(p2head) or p2head in p_bodies:
        print('Player red wins!')
        return

    # Add the current players heads
    p_bodies.add(p1head)
    p_bodies.add(p2head)

    square(p1xy.x, p1xy.y, 3, 'red')
    square(p2xy.x, p2xy.y, 3, 'blue')

    # Update the turtle to draw
    update()

    # Goto next game state
    ontimer(draw, DELAY)


def main():
    # setup screen space dimensions, not synced with playable grid size
    setup(WINDOW_SIZE, WINDOW_SIZE, 370, 0)

    # hide the debug turtle drawer
    hideturtle()

    # this prevents the turtle draw drawing every pixel synchronously,
    # the turtle will be updated at the end of each game state
    tracer(False)

    # enable user input listening, this should be disabled once AI testing starts
    listen()

    # Red Inputs, standard wsad controls for North South West East
    onkey(lambda: movep1(0, SNAKE_SPEED), 'w')
    onkey(lambda: movep1(0, -SNAKE_SPEED), 's')
    onkey(lambda: movep1(-SNAKE_SPEED, 0), 'a')
    onkey(lambda: movep1(SNAKE_SPEED, 0), 'd')

    # Blue Inputs, same as reds inputs but with ikjl (vim like)
    onkey(lambda: movep2(0, SNAKE_SPEED), 'i')
    onkey(lambda: movep2(0, -SNAKE_SPEED), 'k')
    onkey(lambda: movep2(-SNAKE_SPEED, 0), 'j')
    onkey(lambda: movep2(SNAKE_SPEED, 0), 'l')

    # Begin game draw loop
    draw()
    done()


# this just tells python to run the main method
if __name__ == "__main__": main()