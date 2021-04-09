"""Tron, classic arcade game.

Exercises

1. Make the tron players faster/slower.
2. Stop a tron player from running into itself.
3. Allow the tron player to go around the edge of the screen.
4. How would you create a computer player?

"""

from turtle import *
from freegames import square, vector

p1xy = vector(-100, 0)
p1aim = vector(4, 0)
p1body = set()

p2xy = vector(100, 0)
p2aim = vector(-4, 0)
p2body = set()


SPEED = 4
DELAY = 100


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


def inside(head):
    # Return True if head inside screen.
    return -200 < head.x < 200 and -200 < head.y < 200


def draw():
    # Advance players and draw game.
    p1xy.move(p1aim)
    p1head = p1xy.copy()

    p2xy.move(p2aim)
    p2head = p2xy.copy()

    if not inside(p1head) or p1head in p2body or p1head in p1body:
        print('Player blue wins!')
        return

    if not inside(p2head) or p2head in p1body or p2head in p2body:
        print('Player red wins!')
        return


    if inside(p1head) and inside(p2head) and p1head == p2head:
        print('Tie!')
        return

    p1body.add(p1head)
    p2body.add(p2head)

    square(p1xy.x, p1xy.y, 3, 'red')
    square(p2xy.x, p2xy.y, 3, 'blue')
    update()
    ontimer(draw, DELAY)


setup(405, 405, 370, 0)

hideturtle()
tracer(False)
listen()

onkey(lambda: movep1(0, SPEED), 'w')
onkey(lambda: movep1(0, -SPEED), 's')
onkey(lambda: movep1(-SPEED, 0), 'a')
onkey(lambda: movep1(SPEED, 0), 'd')

onkey(lambda: movep2(0, SPEED), 'i')
onkey(lambda: movep2(0, -SPEED), 'k')
onkey(lambda: movep2(-SPEED, 0), 'j')
onkey(lambda: movep2(SPEED, 0), 'l')

draw()
done()