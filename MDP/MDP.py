import random
import math

class MDP:
    
    def __init__(self, 
                 ball_x=None,
                 ball_y=None,
                 velocity_x=None,
                 velocity_y=None,
                 paddle_y=None):
        '''
        Setup MDP with the initial values provided.
        '''
        self.create_state(
            ball_x=ball_x,
            ball_y=ball_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            paddle_y=paddle_y
        )
        
        # the agent can choose between 3 actions - stay, up or down respectively.
        self.actions = [0, 0.04, -0.04]
        
    
    def create_state(self,
              ball_x=None,
              ball_y=None,
              velocity_x=None,
              velocity_y=None,
              paddle_y=None):
        '''
        Helper function for the initializer. Initialize member variables with provided or default values.
        '''
        self.paddle_height = 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        self.paddle_y = 0.5
        self.reward = 0
    
    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''
        # Your Code Goes Here!

        # Update positions
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y
        self.paddle_y += self.actions[action_selected]

        # Collision detection
        if self.paddle_y < 0:
            self.paddle_y = 0
        if(self.paddle_y > (1 - self.paddle_height)):
            self.paddle_y = (1 - self.paddle_height)

        if self.ball_y < 0:
            self.ball_y *= -1
            self.velocity_y *= -1
        if self.ball_y > 1:
            self.ball_y = 2 - self.ball_y
            self.velocity_y *= -1
        if self.ball_x < 0:
            self.ball_x *= -1
            self.velocity_x *= -1
        if self.ball_x > 1:
            if (self.paddle_y+self.paddle_height) >= self.ball_y >= self.paddle_y:
                #bounce back
                self.ball_x = 2 - self.ball_x
                self.velocity_x = -self.velocity_x + random.uniform(-0.015, 0.015)
                self.velocity_y = self.velocity_y + random.uniform(-0.03, 0.03)
                if math.fabs(self.velocity_x <= 0.03):
                    self.velocity_x = 0.04 if self.velocity_x > 0 else -0.04
                self.reward = 1
            else:
                self.reward = -1

        # constraint velocity
        if math.fabs(self.velocity_x > 1):
            self.velocity_x = 1 if self.velocity_x > 0 else -1
        if math.fabs(self.velocity_y > 1):
            self.velocity_y = 1 if self.velocity_y > 0 else -1

        pass
    
    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''
        # Your Code Goes Here!
        dBallX = math.floor(12 * self.ball_x)
        if dBallX >= 12:
            dBallX = 12
        else:
            dBallX = int(dBallX)

        dBallY = int(math.floor(12 * self.ball_y))

        dVelocityX = 1 if self.velocity_x > 0 else -1
        if self.velocity_y > 0.015:
            dVelocityY = 1
        elif self.velocity_y < -0.015:
            dVelocityY = -1
        else:
            dVelocityY = 0

        dPaddleY = math.floor(12 * self.paddle_y / (1 - self.paddle_height))
        if self.paddle_y == 1 - self.paddle_height:
            dPaddleY = 11

        return tuple([dBallX, dBallY, dVelocityX, dVelocityY, dPaddleY])

    def getReward(self):
        dReward = self.reward
        self.reward = 0
        return dReward