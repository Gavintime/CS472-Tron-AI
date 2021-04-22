"""Tron, a classic arcade game.
   This is the Class of the game, each object is a game instance
"""
import time
import turtle
import numpy as np
from freegames import vector
from ai_inputs import dist_totals
from enum import Enum
import copy


class TronGame:

    """GAME CONSTANTS"""
    # speed as in distance traveled after each "frame"
    SNAKE_SPEED = 4
    # this needs to be divisible by SNAKE_SPEED for grids to align properly
    GRID_SIZE = 400
    WINDOW_SIZE = GRID_SIZE + 2

    # enum class for game states
    class GameState(Enum):
        ongoing = 1
        red_won = 2
        blue_won = 3
        tie = 4

    # Default start location/directions
    RED_LOC_DEFAULT = vector(int(GRID_SIZE * .25), int(GRID_SIZE * .5))
    BLUE_LOC_DEFAULT = vector(int(GRID_SIZE * .75), int(GRID_SIZE * .5))
    RED_DIR_DEFAULT = vector(SNAKE_SPEED, 0)
    BLUE_DIR_DEFAULT = vector(-SNAKE_SPEED, 0)

    # Default grid has a wall of bodies around the edges of the grid
    P_BODIES_DEFAULT = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    for col in range(len(P_BODIES_DEFAULT)):
        for row in range(len(P_BODIES_DEFAULT[col])):
            if row == 0 or row == GRID_SIZE - 4 or col == 0 or col == GRID_SIZE - 4:
                P_BODIES_DEFAULT[col][row] = True


    """
        defaults are for player v player, screen must be provided
    """
    def __init__(self, graphics_enable=True,
                 screen=None, keep_window_open=True,
                 ai_red_net=None, ai_blue_net=None,
                 debug_text=False, end_text=False,
                 delay=20):

        """setup values for this game instance"""
        self._graphics_enable = graphics_enable
        self._ai_red = ai_red_net
        self._ai_blue = ai_blue_net
        self._debug_text = debug_text
        self._end_text = end_text
        self._delay = delay

        # starting conditions that have to be copied for each game
        self._red_loc = copy.deepcopy(self.RED_LOC_DEFAULT)
        self._blue_loc = copy.deepcopy(self.BLUE_LOC_DEFAULT)
        self._red_aim = copy.deepcopy(self.RED_DIR_DEFAULT)
        self._blue_aim = copy.deepcopy(self.BLUE_DIR_DEFAULT)
        self._p_bodies = copy.deepcopy(self.P_BODIES_DEFAULT)
        self._state = self.GameState.ongoing

        """Graphical variables, turtles will be set when start_game() is called if in graphical mode"""
        self._screen = screen
        self._t_red = None
        self._t_blue = None
        self._t_draw = None
        # note, this should only be enabled if running a single instance of the game
        self._keep_window_open = keep_window_open
        self._time = 0


    def start_game(self):

        # setup turtle, and inputs if graphical mode
        if self._graphics_enable:

            # (re)set screen
            self._screen.screensize(400, 400, "black")  # sets drawable area of the turtle
            # disable turtle drawing animation for the screen
            self._screen.tracer(False)

            # setup turtles to draw with or display
            turtle.mode("world")
            # This performs a screen.reset()
            turtle.setworldcoordinates(0, 0, self.GRID_SIZE, self.GRID_SIZE)

            # visual head of red
            self._t_red = turtle.Turtle()
            self._t_red.penup()
            self._t_red.color("#FF6600")
            self._t_red.shape("square")
            self._t_red.shapesize(.4)

            # visual head of blue
            self._t_blue = turtle.Turtle()
            self._t_blue.penup()
            self._t_blue.color("#00FFFF")
            self._t_blue.shape("square")
            self._t_blue.shapesize(.4)

            # the turtle that actually draws
            self._t_draw = turtle.Turtle()
            self._t_draw.hideturtle()
            self._t_draw.penup()

            # draw playable area border
            self._t_draw.pensize(5)
            self._t_draw.color("white")
            self._t_draw.setpos(0, 0)
            self._t_draw.setheading(0)
            self._t_draw.pendown()
            self._t_draw.forward(self.GRID_SIZE)
            self._t_draw.setheading(90)
            self._t_draw.forward(self.GRID_SIZE - 4)
            self._t_draw.setheading(180)
            self._t_draw.forward(self.GRID_SIZE)
            self._t_draw.setheading(270)
            self._t_draw.forward(self.GRID_SIZE - 4)
            self._t_draw.pensize(1)

            # Enable inputs for red and blue if there is a player controller
            if self._ai_red is None:
                self._screen.onkey(lambda: self._movep1(0, self.SNAKE_SPEED), 'w')
                self._screen.onkey(lambda: self._movep1(0, -self.SNAKE_SPEED), 's')
                self._screen.onkey(lambda: self._movep1(-self.SNAKE_SPEED, 0), 'a')
                self._screen.onkey(lambda: self._movep1(self.SNAKE_SPEED, 0), 'd')

            if self._ai_blue is None:
                self._screen.onkey(lambda: self._movep2(0, self.SNAKE_SPEED), 'i')
                self._screen.onkey(lambda: self._movep2(0, -self.SNAKE_SPEED), 'k')
                self._screen.onkey(lambda: self._movep2(-self.SNAKE_SPEED, 0), 'j')
                self._screen.onkey(lambda: self._movep2(self.SNAKE_SPEED, 0), 'l')

            # set focus to screen to get inputs if at least one human player
            if self._ai_red is None or self._ai_blue is None: self._screen.listen()


        # begin game state/draw loop
        while self._state == self.GameState.ongoing:
            self._state = self._update()
            time.sleep(self._delay * 0.001)

        # run code here after game ends


        # disable user inputs after game ends if in graphics mode, then keep window open
        if self._graphics_enable:
            if self._ai_red is None:
                self._screen.onkey(None, 'w')
                self._screen.onkey(None, 's')
                self._screen.onkey(None, 'a')
                self._screen.onkey(None, 'd')
            if self._ai_blue is None:
                self._screen.onkey(None, 'i')
                self._screen.onkey(None, 'k')
                self._screen.onkey(None, 'j')
                self._screen.onkey(None, 'l')
            # keep window open after game finishes
            if self._keep_window_open: turtle.done()


    # This returns the fitness of both players for a single game
    # TODO: actually implement a proper fitness function
    def get_fitness(self):
        print(self._time)
        if self._state == self.GameState.tie:
            return [0, 0]
        elif self._state == self.GameState.red_won:
            return [500 + self._time, 0]
        elif self._state == self.GameState.blue_won:
            return [0, 500 + self._time]


    def _update(self):

        self._time += 1

        # draw the head of each snake if graphics enabled
        if self._graphics_enable:
            self._t_draw.color("red")
            self._draw_square(self._red_loc.x, self._red_loc.y)
            self._t_draw.color("blue")
            self._draw_square(self._blue_loc.x, self._blue_loc.y)


        # increment the snake heads in the direction of their current aim
        self._red_loc.move(self._red_aim)
        self._blue_loc.move(self._blue_aim)


        # generate percepts info for ai if enabled
        red_percepts, blue_percepts = None, None
        if self._ai_red or self._ai_blue:
            red_percepts, blue_percepts = dist_totals(self._red_loc, self._blue_loc,
                                                      self._red_aim, self._blue_aim,
                                                      self._p_bodies,
                                                      self.GRID_SIZE,
                                                      self.SNAKE_SPEED)
            # print(red_percepts, blue_percepts)

        # get inputs from AI if enabled
        # The AI takes the game state as an input,
        # the AI outputs the controls (game inputs) to be sent to the game
        if self._ai_red:
            red_controls = self._ai_red.activate(red_percepts)
            # print("red controls: ", red_controls)
            if red_controls[0] >= 0.5: self._movep1(0, self.SNAKE_SPEED)
            if red_controls[1] >= 0.5: self._movep1(0, -self.SNAKE_SPEED)
            if red_controls[2] >= 0.5: self._movep1(-self.SNAKE_SPEED, 0)
            if red_controls[3] >= 0.5: self._movep1(self.SNAKE_SPEED, 0)

        if self._ai_blue:
            blue_controls = self._ai_blue.activate(blue_percepts)
            # print("blue controls: ", blue_controls)
            if blue_controls[0] >= 0.5: self._movep2(0, self.SNAKE_SPEED)
            if blue_controls[1] >= 0.5: self._movep2(0, -self.SNAKE_SPEED)
            if blue_controls[2] >= 0.5: self._movep2(-self.SNAKE_SPEED, 0)
            if blue_controls[3] >= 0.5: self._movep2(self.SNAKE_SPEED, 0)


        # move the visual heads of each snake if graphics enabled
        if self._graphics_enable:
            self._t_red.setpos(self._red_loc.x, self._red_loc.y)
            self._t_blue.setpos(self._blue_loc.x, self._blue_loc.y)


        # alive flags
        red_alive = True
        blue_alive = True

        # Check if Red died
        if self._p_bodies[self._red_loc.x, self._red_loc.y]:
            red_alive = False
        # Check if Blue Died
        if self._p_bodies[self._blue_loc.x, self._blue_loc.y]:
            blue_alive = False

        # end game if either player is dead or hit each other
        if self._red_loc == self._blue_loc or (not red_alive and not blue_alive):
            return self.GameState.tie
        elif not red_alive:
            return self.GameState.blue_won
        elif not blue_alive:
            return self.GameState.red_won

        # print debug info if enabled
        if self._debug_text: print(dist_totals(self._red_loc, self._blue_loc,
                                               self._red_aim, self._blue_aim,
                                               self._p_bodies,
                                               self.GRID_SIZE,
                                               self.SNAKE_SPEED))

        # Add the current players heads to the body array
        self._p_bodies[self._red_loc.x, self._red_loc.y] = True
        self._p_bodies[self._blue_loc.x, self._blue_loc.y] = True

        # update screen and goto next game state
        if self._graphics_enable:
            self._screen.update()

        # game is still ongoing, the loop will then call this function again incrementing the game state
        return self.GameState.ongoing


    def _draw_square(self, x, y):
        self._t_draw.penup()
        self._t_draw.setpos(x + 1, y + 1)
        # self._t_draw.begin_fill()
        self._t_draw.setheading(0)
        self._t_draw.pendown()
        self._t_draw.forward(self.SNAKE_SPEED - 1)
        self._t_draw.setheading(270)
        self._t_draw.forward(self.SNAKE_SPEED - 1)
        self._t_draw.setheading(180)
        self._t_draw.forward(self.SNAKE_SPEED - 1)
        self._t_draw.setheading(90)
        self._t_draw.forward(self.SNAKE_SPEED - 1)
        # self._t_draw.end_fill()
        self._t_draw.penup()


    def _print_grid(self):
        for y in range(self.GRID_SIZE - 4, -1, -4):
            for x in range(0, self.GRID_SIZE, 4):
                if self._p_bodies[x, y]:
                    print('0', end='')
                else:
                    print('.', end='')
            print()
        print(self._red_loc, self._blue_loc)


    def _movep1(self, x, y):
        # ignore moves that go reverse
        if x == self._red_aim.x or y == self._red_aim.y: return
        self._red_aim.x = x
        self._red_aim.y = y
        if self._debug_text: print("Red Turned!")


    def _movep2(self, x, y):
        # ignore moves that go reverse
        if x == self._blue_aim.x or y == self._blue_aim.y: return
        self._blue_aim.x = x
        self._blue_aim.y = y
        if self._debug_text: print("Blue Turned!")