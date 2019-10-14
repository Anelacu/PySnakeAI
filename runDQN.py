from dqn import Agent
import numpy as np
from keras.utils import to_categorical
from random import randint
import pygame
from game_objects import *


class GameLoop:
    def __init__(self, screen, clock):
        self.size = 500
        self.screen = screen
        self.clock = clock
        self.snakeCollide = False
        self.foodCollide = False
        self.over = False

    # check collisions and assign rewards based on collisions
    def check_collisions(self, snake, food):
        # Check collision with food
        if snake.x == food.x and snake.y == food.y:
            snake.snake_grow()
            self.foodCollide = True

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
            snake.x = abs(snake.x % self.size)
            snake.y = abs(snake.y % self.size)
            return True
        # Check collision with self
        else:
            for i, s in enumerate(snake.segments[1:]):
                if s.x == snake.x and s.y == snake.y:
                    segs = [(seg.x, seg.y) for seg in snake.segments]
                    self.snakeCollide = True
                    self.over = True
                    return True

    # Utility function to redraw the window
    def update_window(self, snake, food):
        self.screen.fill(BLACK)
        food.food_draw(self.screen)
        snake.snake_draw()
        pygame.display.update()


    def main_loop(self):
        agent = Agent()
        numGames = 0
        top = 0
        while numGames < 200:
            food = Food(self.size, self.screen)
            food.food_new()
            snake = Snake(size=self.size)
            while not self.over:
                agent.epsilon = 100 - numGames
                oldState = agent.get_state(snake,food)
                if randint(0,200) < agent.epsilon:
                    move = to_categorical(randint(0,2),num_classes=3)
                else:
                    predict = agent.model.predict(state_old.reshape(1,11))
                    move = to_categorical(np.argmax(predict[0]), num_classes=3)
                if np.array_equal(move ,[1, 0, 0]):
                    self.xVel = 10
                elif np.array_equal(move,[0, 1, 0]) and self.y_change == 0:  # right - going horizontal
                    self.yVel = 10
                elif np.array_equal(move,[0, 1, 0]) and self.x_change == 0:  # right - going vertical
                    self.yVel = -10
                elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
                    self.xVel = -10
                elif np.array_equal(move,[0, 0, 1]) and self.x_change == 0:  # left - going vertical
                    self.yVel = 10
                update_window(food,snake)
                self.clock.tick(10)
                newState = agent.get_state(snake,food)
                reward = agent.get_reward(self.foodCollide,self.over)
                agent.train_short(oldState,move,reward,newState,self.over)
                agent.write_memory(oldState,move,reward,newState,self.over)
            agent.replay(agent.memory)
            numGames += 1
            print(numGames)



PURPLE = (255, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
size = 500
# Set screen size and init pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode([size, size])
pygame.init()
game = GameLoop(screen,clock)
game.main_loop()
