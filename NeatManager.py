import os
import pickle

from TronGame import TronGame
import neat
import turtle

# create screen
main_screen = turtle.Screen()
main_screen.setup(402, 402)

# number of generations to train
GENERATIONS = 50

small_gen = 10

def run(config_file):
    # load config file into memory
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # create population
    pop = neat.population.Population(config)

    # enable stats output
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    # begin training, second param is max generation number

    # Trains one generation and saves it
    winner1 = pop.run(eval_genomes, 1)

    # Trains in increments of 10 generations and saves each one
    winner10 = pop.run(eval_genomes, small_gen)

    winner20 = pop.run(eval_genomes, small_gen)

    winner30 = pop.run(eval_genomes, small_gen)

    winner40 = pop.run(eval_genomes, small_gen)

    winner50 = pop.run(eval_genomes, small_gen)

    # Trains for a final 50 generations and saves it
    winnerALL = pop.run(eval_genomes, GENERATIONS)

    # after end of training, store best fit to file
    with open("winnerALL.pkl", "wb") as f:
        pickle.dump(winnerALL, f)  # change to pop if you want best in generation
        f.close()

    with open("winner1.pkl", "wb") as f:
        pickle.dump(winner1, f)
        f.close()

    with open("winner10.pkl", "wb") as f:
        pickle.dump(winner10, f)
        f.close()

    with open("winner20.pkl", "wb") as f:
        pickle.dump(winner20, f)
        f.close()

    with open("winner30.pkl", "wb") as f:
        pickle.dump(winner30, f)
        f.close()

    with open("winner40.pkl", "wb") as f:
        pickle.dump(winner40, f)
        f.close()

    with open("winner50.pkl", "wb") as f:
        pickle.dump(winner50, f)
        f.close()

# this function evaluates each genome, giving it a fitness value
# It does this by having it play tron against other genomes.
# Each genome will play 2 games against every other genome, once as red, then as blue.
# After each game, the fitness from that specific game will be calculated based on if they won or lost,
# as well as how long the game lasted. (and possible other factors)
# The fitness from every game for a genome will then be added together
# to form the genomes total fitness for that generation
def eval_genomes(genomes, config):
    eval_genomes.gen += 1
    # default every genomes fitness to 0
    for _, genome in genomes:
        genome.fitness = 0


    # genomes is a list of genome_id's and genome's,
    for red_id, red_genome in genomes:
        for blue_id, blue_genome in genomes:

            # skip if the same genome
            if red_id == blue_id: continue

            # create a neural network of the current genomes
            red_net = neat.nn.FeedForwardNetwork.create(red_genome, config)
            blue_net = neat.nn.FeedForwardNetwork.create(blue_genome, config)


            # run the game
            # graphically show the last however many generations
            if eval_genomes.gen > (small_gen * 5) + GENERATIONS + 1:  # calculation: total number of generations ran

                game = TronGame(graphics_enable=True, screen=main_screen, keep_window_open=False,
                                ai_red_net=red_net, ai_blue_net=blue_net,
                                debug_text=False, end_text=False, delay=0)
                game.start_game()
                main_screen.clear()

            else:
                game = TronGame(graphics_enable=False, screen=None, keep_window_open=False,
                                ai_red_net=red_net, ai_blue_net=blue_net,
                                debug_text=False, end_text=False, delay=0)
                game.start_game()

            # add to the genomes fitness
            red_genome.fitness += game.get_fitness_wojtek_wall_updated()[0]
            blue_genome.fitness += game.get_fitness_wojtek_wall_updated()[1]

    # divide fitness by the number of games played
    for _, genome in genomes:
        genome.fitness /= (len(genomes) - 1)*2


# static variable
eval_genomes.gen = 0

# get config file path, then run neat
if __name__ == "__main__":
    # get directory of repo
    local_dir = os.path.dirname(__file__)
    # add on the name of the neat config file
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
