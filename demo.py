from Simulator.simulator import Simulator
import sys

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''
    simulator = Simulator(input_file = 'q_table.cfg')
    score = simulator.play_game(False, True)
