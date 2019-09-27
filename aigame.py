from random import choice
from ai_functionality import *
import json


# Segment is a block of the Snake
# The snake is constructed of these segments
class Segment:
    def __init__(self, x, y, width=10):
        self.x, self.y = x, y
        self.width = width


# Food is the objective that snake is meant to reach
# Food will cause the snake to grow and score to increase
class Food:
    def __init__(self, size, x=0, y=0, width=10):
        self.x, self.y = x, y
        self.width = width
        self.size = size

# Update coordinates after the food has been eaten
    def food_new(self):
        self.x = choice(range(10, self.size, self.width))
        self.y = choice(range(10, self.size, self.width))


# Snake class
# Length controls starting number of segments
# self.segments is used to store the segments of the snake
# xVel and yVel are velocities used to determine snake movement
# direction is a label of the current direction of the snake
class Snake:
    def __init__(self, length=5, size=500):
        self.initial_length = length
        self.length = length
        self.segments = []
        self.x, self.y = size//2, size//2
        self.xVel, self.yVel = -10, 0
        for i in range(length):
            self.segments.append(Segment(self.x, self.y))
            self.x += self.segments[i].width

# Function to move the snake
# Tail is popped and new head is drawn
    def snake_move(self):
        self.x += self.xVel
        self.y += self.yVel
        self.segments.insert(0, Segment(self.x, self.y))
        self.segments.pop()

# Function to add a new segment to the snake
# Draws a head in the place of the eaten food
    def snake_grow(self):
        self.x += self.xVel
        self.y += self.yVel
        self.segments.insert(0, Segment(self.x, self.y))

    def snake_reset(self, length=5, size=500):
        self.initial_length = length
        self.length = length
        self.segments = []
        self.x, self.y = size // 2, size // 2
        self.xVel, self.yVel = -10, 0
        for i in range(length):
            self.segments.append(Segment(self.x, self.y))
            self.x += self.segments[i].width


# Reworked game loop to remove unneeded functionality for AI
# Reworked game loop to remove unneeded functionality for AI
class AiLoop:
    def __init__(self,q_table, iterations=1000):
        self.size = 500
        self.reward = -0.1
        self.iterations = iterations
        self.food_collisions = 0
        self.self_collisions = 0
        self.border_collisions = 0
        # Some variables that will be used for q learning
        # For now numbers are just approximations
        self.q_table = q_table
        self.avail_actions = ['up', 'down', 'left', 'right']
        self.learning_rate = 0.15
        self.discount_factor = 0.5
        self.random_rate = 0.1

    # check collisions and assign rewards based on collisions
    def check_collisions(self, snake, food):
        # Check collision with food
        if snake.x == food.x and snake.y == food.y:
            snake.snake_grow()
            self.reward = 2
            self.food_collisions += 1
            on_snake = True
            while on_snake:
                food.food_new()
                on_snake = False
                # Check if the food is not on the snake
                for s in snake.segments[1:]:
                    if s.x == food.x and s.y == food.y:
                        on_snake = True
        # Check collision with borders
        elif snake.x > self.size or snake.x < 0 or snake.y > self.size or snake.y < 0:
            self.reward = -0.1
            self.border_collisions += 1
            snake.x = abs(snake.x % self.size)
            snake.y = abs(snake.y % self.size)
            return True
        # Check collision with self
        else:
            for i, s in enumerate(snake.segments[1:]):
                if s.x == snake.x and s.y == snake.y:
                    segs = [(seg.x, seg.y) for seg in snake.segments]
                    #print(i, "with itself", len(snake.segments), segs)
                    self.reward = -1
                    self.self_collisions += 1
                    return True
            self.reward = -0.1

    # Initialise the loop and create all needed objects
    def loop_init(self):
        food = Food(self.size)
        food.food_new()
        snake = Snake(size=self.size)
        self.main_loop(food, snake)

    def main_loop(self, food, snake):
        for i in range(self.iterations):
            # start loop
            # get state of loop
            # select action from q table
            # get reward
            # update state in q table
            # repeat
            state = select_state(snake, food)
            action = select_action(self.q_table, state, self.random_rate)
            if action == 'up':
                snake.yVel -= 10
                snake.xVel = 0
            elif action == 'down':
                snake.yVel += 10
                snake.xVel = 0
            elif action == 'right':
                snake.xVel += 10
                snake.yVel = 0
            elif action == 'left':
                snake.xVel -= 10
                snake.yVel = 0
            snake.snake_move()
            self.check_collisions(snake, food)
            reward = self.reward
            state_updated = select_state(snake, food)
            q_table_update(self.q_table, state, state_updated, reward,
                           action, self.learning_rate,
                           self.discount_factor, self.random_rate)
            self.check_collisions(snake, food)
            if i % 10 == 0:
                print('Percent loaded: {} %'.format(i*100//self.iterations))
                with open('log.txt', 'a') as log:
                    line0 = '---------------------------------------------------'
                    line1 = 'Iteration # {} '.format(i)
                    line2 = 'Collisions Stats:'
                    line3 = 'Self : {}'.format(self.self_collisions)
                    line4 = 'Food : {}'.format(self.food_collisions)
                    line5 = 'Borders: {}'.format(self.border_collisions)
                    line6 = '---------------------------------------------------'
                    log.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
                        line0, line1, line2,
                        line3, line4, line5, line6))
        with open('q_table.json', 'w', encoding='utf-8') as f:
            json.dump(self.q_table, f, ensure_ascii=False, indent=4)


with open('q_table.json') as f:
    q_table = json.load(f)
iterations = 10000
for i in range(iterations//10):
    print('Loops done ' + str(i))
    ai = AiLoop(q_table,iterations)
    ai.loop_init()
