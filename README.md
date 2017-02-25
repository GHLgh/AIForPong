This readme serves to give an overview of the flow of the project.

### runner.py
Setup the required parameters and start Simulation.

Usage:
```
python runner.py [-h (usage)][-m single/double][-a alpha_value] [-g gamma_value] [-e epsilon_value]
					[-n num_games] [-f input_file] [-s file_to_save_qtable]
	-h 					: print out the usage
	-m single/double 	: training modes
							single - train with single paddle;
							double - train with two paddles against each other
	-a alpha_value		: float  as the learning rate
	-g gamma_value		: float  as the discount factor of next state's utility
	-e epsilon_value	: float  as the chance of randomly exploration
	-n num_games		: int    as the number of games for training
	-f input_file		: string as the file contains different sets of parameters for training (-a,-g,-e,-n)
	-s output_file		: string as the .cfg file to store the trained q table 
							(in the case of -f, only store the table for the last set of parameters)
```

### Simulator
* The broad tasks of the Simulator are to train the agent and then test it on a real game. Ultimately, the agent is embodied in Simulator.
* During the training phase, the goal of the agent is to learn the optimal parameters to ensure as many bounces as possible.
* Training will be done over a certain number of games so the code is modulized to reuse the same code game over game.
* For testing, use the parameters learned on an actualy pong game. Keep playing till the agent loses and track the bounces.

### MDP
* Sets up the Markov Decision Process that includes states, actions, (refer to the documentation for more details) to discretize the game
* Performs actions on states for example, moves the paddle up and the ball in a certain direction.
* Keeps track of 2 kinds of states - continuous and discrete.
