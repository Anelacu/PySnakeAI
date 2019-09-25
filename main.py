from numpy import subtract
import operator
import random
# Some variables that will be used for q learning
# For now numbers are just approximations
q_table = {}
avail_actions = ['up', 'down', 'left', 'right']
learning_rate = 0.85
discount_factor = 0.9
random_rate = 0.05
iterations = 1000


# Function which will return a tuple representing the state
# State = (relative coordinates food to head, relative coordinates tail to head)
def select_state(snake, food):
    head_pos = (snake.segments[0].x, snake.segments[0].y)
    tail_pos = (snake.segments[-1].x, snake.segments[-1].y)
    food_pos = (food.x, food.y)
    tail_rel = tuple(subtract(tail_pos, head_pos))
    food_rel = tuple(subtract(food_pos, head_pos))
    return food_rel, tail_rel


# Function to return the state and its action values
# If state does not exist add it and set action values to 0
def q_table_lookup(state):
    if state in q_table.keys():
        return q_table[state]
    else:
        q_table[state] = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        return q_table[state]


# Function to select best action from a given state
# If all state are 0 return random action
def select_action(state):
    if all(value == 0 for value in state.values()):
        best = random.choice(list(state))
        return best
    else:
        best = max(state.items(), key=operator.itemgetter(1))[0]
    return best


# Function to update the state in the q table
# use select action to estimate the optimal future value
# calculate learned value by adding reward to discount * predicted
# subtract the old value
# then update q table by old value + learning rate*new value
def q_table_update(state0, state1, reward, action):
    q0 = q_table_lookup(state0)
    q1 = q_table_lookup(state1)
    new_val = reward + discount_factor * select_action(q1) - q0[action]
    q_table[state0][action] = q0[action] + learning_rate * new_val


# Function used to fetch the reward value
# game.reward is calculated in game class based on collisions
# if its not 0 it means that some collision state occured so we return reward
# if no value is set then we return -0.1 as a base negative
def get_reward(game):
    if game.reward != 0:
        return game.reward
    else:
        return -0.1

# -------- To Dos -------------
# temp comments
# basic structure of process:
# start game loop
# get state of game loop
# select action from q table
# get reward
# update state in q table
# repeat

# what needs doing:
# 1) we dont actually need to see the screen, so all screen display can be removed
# 2) snake needs to be wired to the algorithm
# 3) need to understand where to init game loop, snake, etc in algorithm
# 4) create some sort of log (maybe txt file) with which we can save q-tables
# 5) and other things to keep track of
# 6) wire everything and test run it
