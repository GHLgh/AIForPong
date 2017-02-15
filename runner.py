from Simulator.simulator import Simulator
import sys

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''
    alpha_value = 0.4
    gamma_value = 0.95
    epsilon_value = 0.04
    if(len(sys.argv) == 4):
        alpha_value = float(sys.argv[1])
        gamma_value = float(sys.argv[2])
        epsilon_value = float(sys.argv[3])
    num_games = 100000
    simulator = Simulator(num_games, alpha_value, gamma_value, epsilon_value)
    target = open("results.txt", 'a')

    totalScore = 0
    highestScore = 0
    for i in range(5):
        score = simulator.play_game(False)
        if score > highestScore:
            highestScore = score
        totalScore += score
        print(score)

    resultForCurrentParameters = "Using alpha = {0}, gamma = {1}, epsilon = {2} and number of games = {3}\nFor playing 5 consecutive games, average score = {4}, highest score = {5}\n\n".format(alpha_value, gamma_value, epsilon_value, num_games, totalScore/5, highestScore)
    target.write(resultForCurrentParameters)
    target.close()
