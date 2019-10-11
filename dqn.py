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


    def get_reward():
        pass
        # need to write function to reward agent


    def network():
        pass
        # need to write function to create actual network


    def write_memory():
        pass
        # need to write function to write to memory of agent


    def replay():
        pass
        # function to replay the games using agent memory


    def train_short():
        pass
        # function to train the short memory
