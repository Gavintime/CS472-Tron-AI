from TronGame import TronGame

import turtle

# create screen
main_screen = turtle.Screen()
main_screen.setup(402, 402)


for i in range(0, 100):
    print("Game Number: ", i+1)
    game = TronGame(graphics_enable=True,
                    screen=main_screen,
                    keep_window_open=False,
                    ai_red_net=None,
                    ai_blue_net=None,
                    delay=30,
                    debug_text=True)
    game.start_game()
    main_screen.clear()
