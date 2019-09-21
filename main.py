from game import *
from numpy import subtract
# Some variables that will be used for q learning
# For now numbers are just approximations
q_table = {}
avail_actions = ['up', 'down', 'left', 'right']
learning_rate = 0.85
dicount_factor = 0.9
random_rate = 0.05


# Function which will return a tuple representing the state
# State = (relative coordinates food to head, relative coordinates tail to head)
def select_state(snake, food):
    head_pos = (snake.segments[0].x, snake.segments[0].y)
    tail_pos = (snake.segments[-1].x, snake.segments[-1].y)
    food_pos = (food.x, food.y)
    tail_rel = tuple(subtract(tail_pos, head_pos))
    food_rel = tuple(subtract(food_pos, head_pos))
    return (food_rel, tail_rel)
