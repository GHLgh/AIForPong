from MDP.MDP import MDP
from MDP.MDPMultiple import MDPMultiple
#from graphics import *
import random
import ConfigParser

class Simulator:
    
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0, import_q_table = ''):
        '''
        Setup the Simulator with the provided values.
        :param num_games - number of games to be trained on.
        :param alpha_value - 1/alpha_value is the decay constant.
        :param gamma_value - Discount Factor.
        :param epsilon_value - Probability value for the epsilon-greedy approach.
        '''
        self.num_games = num_games       
        self.epsilon_value = epsilon_value       
        self.alpha_value = alpha_value       
        self.gamma_val = gamma_value
        
        # Your Code Goes Here!
	self.construct_q_table(import_q_table)

        '''
        self.win = GraphWin("Pong Game", 700, 700)
        self.ball = Circle(Point(350, 350), 20)
        msg = Text(Point(330, 25), "Pong Game")
        msg.draw(self.win)
        for i in range(0, 12):
            for j in range(0, 12):
                c = Rectangle(Point(50 + i * 50, 50 + j * 50), Point(100 + i * 50, 100 + j * 50))
                c.draw(self.win)
        self.p = Rectangle(Point(600, 250), Point(650, 400))
        self.p.setFill("red")
        self.p.draw(self.win)
        self.ball.draw(self.win)
        '''
    def construct_q_table(self):
	config = ConfigParser.RawConfigParser()
	config.read('stage.cfg')

	# getfloat() raises an exception if the value is not a float
	# getint() and getboolean() also do this for their respective types
	self.stage_x = config.getint('DiscreteState', 'stage_x')
	self.stage_y = config.getint('DiscreteState', 'stage_y')
	self.velocity_x = config.getint('DiscreteState', 'velocity_x')
        self.velocity_y = config.getint('DiscreteState', 'velocity_y')
	#TODO enable velocity part
	self.QTable = {}
	# Init the Q Table to be all zeros
	for ballX in range(self.stage_x):
	    for ballY in range(self.stage_y):
		for velocityX in [-1, 1]:
		    for velocityY in [-1, 0, 1]:
			for paddleY in range(self.stage_y):
			    for action in range(3):
				key = tuple([ballX, ballY, velocityX, velocityY, paddleY, action])
				self.QTable[key] = 0
	self.QTable[-1] = 0 
	pass   

    def export_q_table(self, file_name):
	config = ConfigParser.RawConfigParser()

	config.add_section('DiscreteState')
	config.set('DiscreteState', 'stage_x', str(self.stage_x))
	config.set('DiscreteState', 'stage_y', str(self.stage_y))
	config.set('DiscreteState', 'velocity_x', str(self.velocity_x))
	config.set('DiscreteState', 'velocity_y', str(self.velocity_y))

	config.add.section("QTable")
	

	# Writing our configuration file to 'example.cfg'
	with open('example.cfg', 'wb') as configfile:
	    config.write(configfile)	

    def f_function(self, currentState, epsilonOn):
        '''
        Choose action based on an epsilon greedy approach
        :return action selected
        '''

        # select random action
        action_selected = None

        # Your Code Goes Here!
        action_selected = random.randint(0,2)

        action0 = currentState + (0,)
        action1 = currentState + (1,)
        action2 = currentState + (2,)

        qlist = [self.QTable[action0], self.QTable[action1], self.QTable[action2]]

        actionSelectedWithGreedy = 0 if qlist[0] > qlist[1] else 1
        actionSelectedWithGreedy = 2 if qlist[2] > qlist[actionSelectedWithGreedy] else actionSelectedWithGreedy

        x = random.random()
        if(x < self.epsilon_value and epsilonOn):
            return action_selected
        else:
            return  actionSelectedWithGreedy

    def train_agent(self, multiplePaddles):
        '''
        Train the agent over a certain number of games.
        '''
        # Your Code Goes Here!
        totalScore = 0
	continueOverTen = 0
	count = -1
        for i in range(self.num_games):
            score = self.play_game(True) if multiplePaddles == False else self.play_game_paddles(True)
            totalScore += score
            if (i+1)%100 == 0:
		if (totalScore/100) >= 10:
		    continueOverTen += 1
		    if continueOverTen >= 3 and count == -1:
			count = i
                print("Average score over last 100 runs: {0}. Ran {1} training, {2} runs remaining".format(totalScore/100,i+1, self.num_games - i-1))
                totalScore = 0
	print(count)
	print("\n")
        pass

    def play_game_paddles(self, training):
        '''
        Simulate an actual game till the agent loses.
        '''
        # Your Code Goes Here!
        environment = MDPMultiple()
        score = 0
        currentStates = [environment.discretize_state(0), environment.discretize_state(1)]
        currentRewards = environment.getReward()

        while(currentRewards[0] != -1 and currentRewards[1] != -1):
            if currentRewards[0] == 1 or currentRewards[1] == 1:
                score += 1

            lastStates = currentStates
            lastRewards = currentRewards
            actionsSelected = [self.f_function(currentStates[0], training),self.f_function(currentStates[1], training)]
            #print("S1:{0} A1:{1}; S2:{2} A2:{3}".format(currentStates[0], actionsSelected[0],currentStates[1], actionsSelected[1]))
            environment.simulate_one_time_step(actionsSelected)
            currentStates = [environment.discretize_state(0), environment.discretize_state(1)]

            self.updateQTable(lastStates[0], actionsSelected[0], lastRewards[0], currentStates[0])
	    self.updateQTable(lastStates[1], actionsSelected[1], lastRewards[1], currentStates[1])

            currentRewards = environment.getReward()

            # special casse to update special stage
            if currentStates[0][0] == 12 or currentStates[1][0] == 12:
                self.QTable[-1] += self.alpha_value * (currentRewards[0] + currentRewards[1] - self.QTable[-1])

            '''
            if training == False:
                time.sleep(0.05)
                self.draw_gui(currentState, lastState)
            '''
	#print("End game\n")
        return score
    
    def play_game(self, training):
        '''
        Simulate an actual game till the agent loses.
        '''
        # Your Code Goes Here!
        environment = MDP()
        score = 0
        currentState = environment.discretize_state()
        currentReward = environment.getReward()

        while(currentReward != -1):
            if currentReward == 1:
                score += 1
            lastState = currentState
            lastReward = currentReward
            actionSelected = self.f_function(currentState, training)
            environment.simulate_one_time_step(actionSelected)
            currentState = environment.discretize_state()
            self.updateQTable(lastState, actionSelected, lastReward, currentState)
            currentReward = environment.getReward()

	    # special casse to update special stage
	    if currentState[0] == 12:
		self.QTable[-1] += self.alpha_value * (currentReward - self.QTable[-1])

            '''
            if training == False:
                time.sleep(0.05)
                self.draw_gui(currentState, lastState)
            '''
        return score

    def updateQTable(self, lastState, actionSelected, lastReward, currentState):
        QLast = self.QTable[lastState + (actionSelected,)]
        if currentState[0] == 12:
            QOptimalCurrent = self.QTable[-1]
        else:
            QOptimalCurrent = self.QTable[currentState + (self.f_function(currentState,False),)]
        #print(type(lastReward))
        self.QTable[lastState + (actionSelected,)] = QLast + self.alpha_value * (lastReward + self.gamma_val * QOptimalCurrent - QLast)
        pass

    def draw_gui(self, cur, pre):
        '''
        x = cur[0] - pre[0]
        y = cur[1] - pre[1]

        # Draw ball
        self.ball.undraw()
        self.ball = Circle(Point(50 + 50 * cur[0] + 25, 50 + 50 * cur[1] + 25), 20)
        self.ball.draw(self.win)
        self.p.undraw()

        # Draw paddle
        self.p = Rectangle(Point(600, 50 * cur[4]), Point(650, 50 * cur[4] + 120))
        self.p.setFill("red")
        self.p.draw(self.win)
        '''
