import os
import pickle
import neat
import turtle
from TronGame import TronGame

# create screen
main_screen = turtle.Screen()
main_screen.setup(402, 402)


# change the file name to which generation's best you want to play
def replay_genome(config_file, genome_path="winnerALL.pkl"):
    # Load required NEAT config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    # Unpickle the winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # create network from winner genome
    blue_net = neat.nn.FeedForwardNetwork.create(genome, config)

    # play against genome as red
    while True:
        game = TronGame(graphics_enable=True,
                        screen=main_screen,
                        keep_window_open=False,
                        ai_red_net=None,
                        ai_blue_net=blue_net,
                        delay=100,
                        debug_text=False,
                        end_text=False)
        game.start_game()
        main_screen.clear()


# get directory of repo
local_dir = os.path.dirname(__file__)
# add on the name of the neat config file
config_path = os.path.join(local_dir, "config-feedforward.txt")
# load genome and have it play blue
replay_genome(config_path)
