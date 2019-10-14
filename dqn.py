from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import pandas as pd
import numpy as np


# ----- ToDo list ---------
# Need to fill out the function skeleton below
# Connect this to game
# Test
# Create some sort of logging system
# Create way to save weights (possibly h5)
# Possibly create a way to load saved weights into network
# Proposed state layout :
# direction of snake (4) if food is below,above,etc (4)
# danger up,down,straight (3) -> all toegther 11 input nodes
 class agent():
    def __init__(self):
        self.reward = 0
        self.gamma = 0
        self.epsilon = 0
        self.learning_rate = 0.005
        self.target = 1
        self.prediction = 0
        self.mem = []
        self.actual = []
        self.memShort = np.array([])
        self.df = pd.DataFrame()
        self.model = self.network()


# function used to get the current state of the agent
    def get_state(self,snake,food):
        aheadDanger = False
        leftDanger = False
        rightDanger = False
        # First get current positions
        curHeadx = snake.segments[0].x
        curHeady = snake.segments[0].y
        curFood = (food.x, food.y)
        # Calculate changes in needed directions
        aheadx = curHeadx + snake.xVel
        aheady = curHeady + snake.yVel
        side1x = curHeadx + snake.yVel
        side1y = curHeadx + snake.xVel
        side2x = curHeadx - snake.yVel
        side2y = curHeadx - snake.xVel
        # Check if there will be collisions on self
        for seg in snake.segments[1:]:
            if aheadx == seg.x and aheady == seg.y:
                aheadDanger = True
            elif side1x == seg.x and side1y == seg.y:
                rightDanger = True
            elif side2x == seg.x and side2y == seg.y:
                leftDanger = True

        # Determine current snake direction
        snakeUp = (snake.yVel == -10)
        snakeDown = (snake.yVel == 10)
        snakeLeft = (snake.xVel == -10)
        snakeRight = (snake.xVel == 10)
        # Determine relative position of food
        foodUp = (food.y < snake.y)
        foodDown = (food.y > snake.y)
        foodLeft = (food.x < snake.x)
        foodRight = (food.x > snake.x)

        state = [aheadDanger,leftDanger,rightDanger,
                 snakeUp,snakeDown,snakeLeft,snakeRight,
                 foodDown,foodUp,foodLeft,foodRight]

        # Normalise data to 0 or 1         
        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0

        return np.assarray(state)


    # Function that will be used to assign reward to agent
    # Reward is normalised to be in range of [-1,1]
    def get_reward(self,snake):
        self.reward = snake.reward
        if self.reward >= 1:
            self.reward = 1
        elif self.reward <= -1:
            self.reward = -1

    # The neural network that will control the agent
    # Consists of dense layers of 120 neurons each and dropout layers
    # ---ToDo--- ---> when state is decided change input dims
    def network(self):
        model = Sequential()
        model.add(Dense(output_dim=120,activation='relu',input_dim=11))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120,activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120,activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120,activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse',optimizer=opt)


    def write_memory():
        pass
        # need to write function to write to memory of agent


    def replay():
        pass
        # function to replay the games using agent memor


    def train_short():
        pass
        # function to train the short memory
