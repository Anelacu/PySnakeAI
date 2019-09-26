from numpy import subtract
import operator
import random
# Some variables that will be used for q learning
# For now numbers are just approximations
learning_rate = 0.5
discount_factor = 0.9
random_rate = 0.05


# Function which will return a tuple representing the state
# State = (relative coordinates food to head, relative coordinates tail to head)
def select_state(snake, food):
    border = 0
    head_pos = (snake.segments[0].x, snake.segments[0].y)
    tail_pos = (snake.segments[-1].x, snake.segments[-1].y)
    food_pos = (food.x, food.y)
    if snake.x > 500 or snake.x < 0 or snake.y > 500 or snake.y < 0: # TODO magic numbers
        border = 1
    tail_rel = tuple(subtract(tail_pos, head_pos))
    food_rel = tuple(subtract(food_pos, head_pos))
    return food_rel, tail_rel


# Function to return the state and its action values
# If state does not exist add it and set action values to 0
def q_table_lookup(table, state):
    if state in table.keys():
        return table[state]
    else:
        table[state] = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        return table[state]


# Function to select best action from a given state
# If all state are 0 return random action
def select_action(table, state):
    states = q_table_lookup(table, state)
    if random.choice(range(0, 100))/100 < random_rate:
        return random.choice(list(states.keys()))
    if all(value == 0 for value in states.values()):
        best = random.choice(list(states.keys()))
    else:
        best = max(states.items(), key=operator.itemgetter(1))[0]
    return best


# Function to update the state in the q table
# use select action to estimate the optimal future value
# calculate learned value by adding reward to discount * predicted
# subtract the old value
# then update q table by old value + learning rate*new value
def q_table_update(table, state0, state1, reward, action):
    q0 = q_table_lookup(table, state0)
    q1 = q_table_lookup(table, state1)
    new_val = reward + discount_factor * q1[select_action(table, state1)] - q0[action]
    table[state0][action] = q0[action] + learning_rate * new_val
