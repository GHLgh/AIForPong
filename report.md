# Report
Q Learning as a reinforcement learning method, it map the different states (maybe continuous) in the problem into a finite set of discrete states.
### Project Idea
In the case of Pong game, which is this project based on, the problem (the display of field, ball and paddle) is continuous. So we try to map the problem into MDP such that we can apply Q learning to the agent.

The intuition is that if the number of discrete states approaches infinity, the MDP can simulate the real problem better, such that the agent can literally use the Q Table to look up every optimal action given a stetes.

So the project is set up in a way that user can change the configuration of how large a Q Table is used in the training.
However, average score of agent trained with the configuration used x = 32, y = 32, vx = 4, vy = 4 has unsignificant than the average score of agent trained with default configuration x = 12, y = 12, vx = 1, vy = 1, which is against the intuition.

Possible reasons are:
* Large Q Table requires more runs to "fill up" the whole table
* The learning rate is not small enough such that gradient decent actually could not converge. In this case, the learning result of more states will be similar to the result of less states (possilbe but not sure)
What is more, the obvious downside of larger Q Table is that more bytes are needed to store the table, not to mention storing it into memory when the applicatioin is running (also the overhead of loading/saving the table is huge)

### Possible Updates
* Interactive interface (Web/Python) for users to play with the trained agent
* Better Q Table (using different approaches to discretalize states)
* Better exploring policy (gaussin distribution rather than random selection)
