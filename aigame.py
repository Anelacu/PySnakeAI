from game import Food
from game import Snake
from ai_functionality import *


# Reworked game loop to remove unneeded functionaility for AI
class AiLoop:
    def __init__(self):
        self.colours = {"PURPLE": (255, 0, 255),
                        "RED": (255, 0, 0),
                        "BLACK": (0, 0, 0)}
        self.size = 500
        self.screen = pygame.display.set_mode([self.size, self.size])
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


    # Initialise the loop and craete all needed objects
    def loop_init(self):
        pygame.init()
        clock = pygame.time.Clock()
        food = Food(self.colours, self.screen, self.size)
        food.food_new()
        snake = Snake(self.colours["PURPLE"], self.screen)
        self.game_loop(clock, food, snake)


    def main_loop(self, clock, food, snake):
        while True:
            # -------- To Dos -------------
            # basic structure of process:
            # start loop
            # get state of loop
            # select action from q table
            # get reward
            # update state in q table
            # repeat

            # what needs doing:
            # 1) we dont actually need to see the screen, so all screen display can be removed (x)
            # 2) snake needs to be wired to the algorithm
            # 3) need to understand where to init game loop, snake, etc in algorithm
            # 4) create some sort of log (maybe txt file) with which we can save q-tables
            # 5) and other things to keep track of
            # 6) wire everything and test run it
            snake.snake_move()
            self.check_collisions(snake, food):
            clock.tick(10)
