from MDP.MDP import MDP
#from graphics import *
import random

class Simulator:
    
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0):
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
        self.QTable = {}

        # Init the Q Table to be all zeros
        for ballX in range(12):
            for ballY in range(12):
                for velocityX in [-1, 1]:
                    for velocityY in [-1, 0, 1]:
                        for paddleY in range(12):
                            for action in range(3):
                                key = tuple([ballX, ballY, velocityX, velocityY, paddleY, action])
                                self.QTable[key] = 0
        self.QTable[-1] = -1
        self.train_agent()

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

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        # Your Code Goes Here!
        totalScore = 0
        for i in range(self.num_games):
            score = self.play_game(True)
            totalScore += score
            if (i+1)%100 == 0:
                print("Average score over last 100 runs: {0}. Ran {1} training, {2} runs remaining".format(totalScore/100,i+1, self.num_games - i-1))
                totalScore = 0
        pass
    
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