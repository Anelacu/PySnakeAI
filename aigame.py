from random import choice
from ai_functionality import *
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
        self.direction = 'LEFT'
        for i in range(length):
            self.segments.append(Segment(self.screen, self.x, self.y, self.colour))
            self.x += self.segments[i].width

# Function to move the snake
# Tail is popped and new head is drawn
    def snake_move(self):
        self.x += self.xVel
        self.y += self.yVel
        self.segments.insert(0, Segment(self.screen, self.x, self.y, self.colour))
        self.segments.pop()

# Function to add a new segment to the snake
# Draws a head in the place of the eaten food
    def snake_grow(self):
        self.x += self.xVel
        self.y += self.yVel
        self.segments.insert(0, Segment(self.screen, self.x, self.y, self.colour))


# Reworked game loop to remove unneeded functionality for AI
class AiLoop:
    def __init__(self):
        self.size = 500
        self.reward = -0.1

    # check collisions and assign rewards based on collisions
    def check_collisions(self, snake, food):
        # Check collision with food
        if snake.x == food.x and snake.y == food.y:
            snake.snake_grow()
            reward = 1
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
            reward = -1
            return True
        # Check collision with self
        else:
            for s in snake.segments[1:]:
                if s.x == snake.x and s.y == snake.y:
                    reward = -1
                    return True

    # Initialise the loop and create all needed objects
    def loop_init(self):
        food = Food(self.colours, self.screen, self.size)
        food.food_new()
        snake = Snake(self.colours["PURPLE"], self.screen)
        self.game_loop(food, snake)

    def main_loop(self, clock, food, snake):
        while True:
            # start loop
            # get state of loop
            # select action from q table
            # get reward
            # update state in q table
            # repeat
            state = select_state(snake,food)
            action = select_action(state)
            if action == 'up':
                snake.direction = 'UP'
                snake.yVel -= 10
                snake.xVel = 0
            elif action == 'down':
                snake.direction = 'DOWN'
                snake.yVel += 10
                snake.xVel = 0
            elif action == 'right':
                snake.direction = 'RIGHT'
                snake.xVel += 10
                snake.yVel = 0
            elif action == 'left':
                snake.direction = 'LEFT'
                snake.xVel -= 10
                snake.yVel = 0
            snake.snake_move()
            self.check_collisions(snake, food)
            reward = AiLoop.reward
            state_updated = select_state(snake,food)
            q_table_update(state, state_updated, reward, action)
            
            # -------- To Dos -------------
            # what needs doing:
            # 1) we dont actually need to see the screen, so all screen display can be removed (x)
            # 2) snake needs to be wired to the algorithm
            # 3) need to understand where to init game loop, snake, etc in algorithm
            # 4) create some sort of log (maybe txt file) with which we can save q-tables
            # 5) and other things to keep track of
            # 6) wire everything and test run it
            self.check_collisions(snake, food)
            clock.tick(10)
