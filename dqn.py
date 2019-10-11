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
class agent():
    def __init__(self):
        self.reward = 0
        self.gamma = 0
        self.epsilon = 0
        self.lambda = 0.005
        self.target = 1
        self.prediction = 0
        self.mem = []
        self.actual = []
        self.memShort = np.array([])
        self.df = pd.DataFrame()
        self.model = self.network()


    def get_state():
        pass
        # need to write func to get state and decide on new
        # state structure


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
        model.add(Dense(output_dim=120,activation='relu',input_dim=1))
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
