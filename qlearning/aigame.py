from random import choice
from ai_functionality import *
import json
import pygame
import sys
import math

PURPLE = (255, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
size = 500

# Set screen size and init pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode([size, size])
pygame.init()

# Segment is a block of the Snake
# The snake is constructed of these segments


class Segment:
    def __init__(self, x, y, width=10, colour=PURPLE):
        self.x, self.y = x, y
        self.width = width
        self.colour = colour


# Draw the segment at the specified coordinates
# Segments are squares with dimensions of width*width

    def segment_draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width,
                                               self.width), 0)


# Food is the objective that snake is meant to reach
# Food will cause the snake to grow and score to increase
class Food:
    def __init__(self, colour=RED, x=0, y=0, width=10, size=500):
        self.x, self.y = x, y
        self.width = width
        self.size = size
        self.colour = colour

# Update coordinates after the food has been eaten
    def food_new(self):
        self.x = choice(range(10, self.size, self.width))
        self.y = choice(range(10, self.size, self.width))


# Draw the food at the specified coordinates
# Food is a square of width*width dimension
    def food_draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y,
                                               self.width, self.width), 0)


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
        self.xVel, self.yVel = 0, 0
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
        self.segments.pop()

    def snake_reset(self, length=5, size=500):
        self.initial_length = length
        self.length = length
        self.segments = []
        self.x, self.y = size // 2, size // 2
        self.xVel, self.yVel = -10, 0
        for i in range(length):
            self.segments.append(Segment(self.x, self.y))
            self.x += self.segments[i].width

    # Function to create the snake

    def snake_draw(self):
        for i in range(len(self.segments)):
            self.segments[i].segment_draw()
            self.length = len(self.segments)


# Reworked game loop to remove unneeded functionality for AI
class AiLoop:
    def __init__(self, q_table, screen, clock, visuals=False, iterations=1000):
        self.size = 500
        self.reward = -0.1
        self.iterations = iterations
        self.food_collisions = 0
        self.self_collisions = 0
        self.border_collisions = 0
        self.screen = screen
        self.clock = clock
        # Some variables that will be used for q learning
        # For now numbers are just approximations
        self.q_table = q_table
        self.avail_actions = ['up', 'down', 'left', 'right']
        self.learning_rate = 0.1
        self.discount_factor = 0.1
        self.random_rate = 0.1

    # check collisions and assign rewards based on collisions
    def check_collisions(self, snake, food):
        # Check collision with food
        if snake.x == food.x and snake.y == food.y:
            snake.snake_grow()
            self.reward = 1
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
                    self.reward = -1
                    self.self_collisions += 1
                    return True
            self.reward = -0.1

    # Initialise the loop and create all needed objects
    def loop_init(self):
        food = Food(self.size, self.screen)
        food.food_new()
        snake = Snake(size=self.size)
        self.main_loop(food, snake)

    # Utility function to redraw the window
    def update_window(self, snake, food):
        self.screen.fill(BLACK)
        food.food_draw(self.screen)
        snake.snake_draw()
        pygame.display.update()

    def main_loop(self, food, snake):
        old_distance = 0
        for i in range(self.iterations):
            # start loop
            # get state of loop
            # select action from q table
            # get reward
            # update state in q table
            # repeat
            head_pos = (snake.segments[0].x, snake.segments[0].y)
            food_pos = (food.x, food.y)
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(
                head_pos, food_pos)]))

            state = select_state(snake, food)
            action = select_action(self.q_table, state, self.random_rate)
            if action == 'up' and snake.yVel != 10:
                snake.yVel = -10
                snake.xVel = 0
            elif action == 'down'and snake.yVel != -10:
                snake.yVel = 10
                snake.xVel = 0
            elif action == 'right' and snake.xVel != -10:
                snake.xVel = 10
                snake.yVel = 0
            elif action == 'left' and snake.yVel != 10:
                snake.xVel = -10
                snake.yVel = 0
            # If manual stop of algorithm is required
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            snake.snake_move()
            self.check_collisions(snake, food)
            reward = self.reward
            if distance < old_distance:
                self.reward += 0.1
            state_updated = select_state(snake, food)
            q_table_update(self.q_table, state, state_updated, reward,
                           action, self.learning_rate,
                           self.discount_factor, self.random_rate)
            self.check_collisions(snake, food)
            self.update_window(snake, food)
            old_distance = distance
            self.clock.tick(100)

            # Create a log file
            if i % 10 == 0:
                with open('log.txt', 'a') as log:
                    line0 = '-------------------------------------------------'
                    line1 = 'Iteration # {} '.format(i)
                    line2 = 'Collisions Stats:'
                    line3 = 'Self : {}'.format(self.self_collisions)
                    line4 = 'Food : {}'.format(self.food_collisions)
                    line5 = 'Borders: {}'.format(self.border_collisions)
                    line6 = '-------------------------------------------------'
                    log.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
                        line0, line1, line2,
                        line3, line4, line5, line6))

        # write q table to a json file
        with open('q_table.json', 'w', encoding='utf-8') as f:
            json.dump(self.q_table, f, ensure_ascii=False, indent=4)


# Function used to run ai training
def run_iteration(iters):
    for i in range(iters):
        print('Loops done ' + str(i))
        ai = AiLoop(q_table, screen, clock, iters)
        ai.loop_init()


# save q table to json
with open('q_table.json') as f:
    q_table = json.load(f)

run_iteration(100)
