import os
import pickle
import neat
import turtle

# create screen
main_screen = turtle.Screen()
main_screen.setup(402, 402)


def replay_genome(configPath, genome_path="winner.pkl"):
    # Load required NEAT config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configPath
    )

    # Unpickle the winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
        
    blue_net = neat.nn.FeedForwardNetwork.create(genome, config)

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
