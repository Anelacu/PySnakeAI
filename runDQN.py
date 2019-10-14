from dqn import agent
import numpy as np
from keras.utils import to_categorical
from random import randint
import pygame

def run():
    pygame.init()
    agent = agent()
    gamesCount = 0
    while gamesCount < 200:
        snake = Snake()
        food = Food()
        # ----- ToDO rewrite a collision function that can be used here ----
        # --- Complete run based on this -----
