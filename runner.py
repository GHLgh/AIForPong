from Simulator.simulator import Simulator
import sys

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''

    # Helper function to parse input file, return false if input file can not be opened
    # and assuming that if input file can be opened, the parameters for each training are written in one line
    # in following format: "alpha_value gamma_value epsilon_value"
    def readInputFile(parameterList, inputFileName):
	try:
            inputFile = open(inputFileName, 'r')
        except IOError:
            print('cannot open', inputFileName)
	    return False;
        else:
	    inputParameters = inputFile.readlines()
	    for line in inputParameters:
		parametersValues = line.split(' ')
		parameterList.append((float(parametersValues[0]),float(parametersValues[1]),float(parametersValues[2]),int(parametersValues[3])))
        inputFile.close()

	return True;

    # process user input, or use default values if user doesn't specify parameters
    parameterList = []
    alpha_value = 0.4
    gamma_value = 0.95
    epsilon_value = 0.04
    num_games = 100000
    outputFileName = "results.txt"
    outputMode = 'w'

    two = False

    if(len(sys.argv) != 2):
	outputMode = 'a'
	if(6 >= len(sys.argv) >= 5):
	    alpha_value = float(sys.argv[1])
            gamma_value = float(sys.argv[2])
            epsilon_value = float(sys.argv[3])
	    num_games = int(sys.argv[4])
	parameterList.append((alpha_value, gamma_value, epsilon_value, num_games));
	if len(sys.argv) == 6:
	    two = True
	    #outputFileName = sys.argv[5]
    elif len(sys.argv) == 2:
	readInputFile(parameterList, sys.argv[1]);
	outputFileName = "out_" + sys.argv[1];

    target = open(outputFileName, outputMode)
    for parameters in parameterList:
	alpha_value = parameters[0]
	gamma_value = parameters[1]
	epsilon_value = parameters[2]
	num_games = parameters[3]
    	simulator = Simulator(num_games, alpha_value, gamma_value, epsilon_value, two)

    	totalScore = 0
    	highestScore = 0
    	for i in range(5):
            score = simulator.play_game(False)
            if score > highestScore:
            	highestScore = score
            totalScore += score

	resultForCurrentParameters = "Using alpha = {0}, gamma = {1}, epsilon = {2} and number of games = {3}\nFor playing 5 consecutive games, average score = {4}, highest score = {5}\n\n".format(alpha_value, gamma_value, epsilon_value, num_games, totalScore/5, highestScore)
        target.write(resultForCurrentParameters)
    target.close()
