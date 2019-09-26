import pygame
from random import choice
from sys import exit


# Segment is a block of the Snake
# The snake is constructed of these segments
class Segment:
    def __init__(self, screen, x, y, colour, width=10):
        self.x, self.y = x, y
        self.colour = colour
        self.width = width
        self.screen = screen

# Draw the segment at the specified coordinates
# Segments are squares with dimensions of width*width
    def segment_draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width,
                                                    self.width), 0)


# Food is the objective that snake is meant to reach
# Food will cause the snake to grow and score to increase
class Food:
    def __init__(self, colours, screen, size, x=0, y=0, width=10):
        self.x, self.y = x, y
        self.colour = colours['RED']
        self.width = width
        self.screen = screen
        self.size = size

# Draw the food at the specified coordinates
# Food is a square of width*width dimension
    def food_draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y,
                                                    self.width, self.width), 0)

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
    def __init__(self, colour, screen, length=5, size=500):
        self.colour = colour
        self.initial_length = length
        self.length = length
        self.screen = screen
        self.segments = []
        self.x, self.y = size//2, size//2
        self.xVel, self.yVel = -10, 0
        self.direction = 'LEFT'
        for i in range(length):
            self.segments.append(Segment(self.screen, self.x, self.y, self.colour))
            self.x += self.segments[i].width

# Function to create the snake
    def snake_draw(self):
        for i in range(len(self.segments)):
            self.segments[i].segment_draw()
            self.length = len(self.segments)

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


class Game:
    def __init__(self):
        self.colours = {"PURPLE": (255, 0, 255),
                        "RED": (255, 0, 0),
                        "BLACK": (0, 0, 0)}
        self.font_name = pygame.font.match_font('arial')
        self.size = 500
        self.screen = pygame.display.set_mode([self.size, self.size])


    # Utility function to display text on the screen
    def draw_text(self, surf, text, fsize, x, y):
        font = pygame.font.Font(self.font_name, fsize)
        text_surface = font.render(text, True, self.colours['PURPLE'])
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    # The start screen
    # If key pressed, start screen loop terminates and game loop begins

    def start_screen(self):
        terminate = False
        while not terminate:
            self.screen.fill(self.colours['BLACK'])
            self.draw_text(self.screen, 'Press any key to play!', 40, 250, 150)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    terminate = True
                    break
                pygame.display.flip()

    # Function to check for snake's collisions with other elements
    # Returns True if the game was lost
    def check_collisions(self, snake, food):
        # Check collision with food
        if snake.x == food.x and snake.y == food.y:
            snake.snake_grow()
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
            return True
        # Check collision with self
        else:
            for s in snake.segments[1:]:
                if s.x == snake.x and s.y == snake.y:
                    return True

    # Utility function to redraw the window
    def update_window(self, snake, food):
        self.screen.fill(self.colours['BLACK'])
        food.food_draw()
        snake.snake_draw()
        # The score = delta length
        self.draw_text(self.screen, str(snake.length-snake.initial_length),
                       30, 250, 10)
        pygame.display.update()

    # Utility function for initialising game objects
    # Starts the game loop

    def game_init(self):
        pygame.init()
        self.start_screen()
        clock = pygame.time.Clock()
        food = Food(self.colours, self.screen, self.size)
        food.food_new()
        food.food_draw()
        snake = Snake(self.colours["PURPLE"], self.screen)
        self.game_loop(clock, food, snake)

    # The game over screen
    # Displayed when game is lost
    # Allows user to play the game again
    def game_over_screen(self, snake):
        self.screen.fill(self.colours['BLACK'])
        self.draw_text(self.screen, "Game over :(", 40, 250, 100)
        self.draw_text(self.screen, "Total score of "+str(
            snake.length-snake.initial_length), 40, 250, 150)
        self.draw_text(self.screen, 'Press any key to play again!', 40, 250, 200)
        pygame.display.update()
        terminate = False
        while not terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    terminate = True
                    break
                pygame.display.flip()
        self.game_init()

    # Game loop
    def game_loop(self, clock, food, snake):
        while True:
            # Get key press
            # Give ability to quit using the x in the window corner
            # Key directions determine velocity of the snake and current direction
            # Snake can not go in same direction as its currently going
            # To avoid stacking of velocities and infinite acceleration
            # Snake can not move in opposite direction to current
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_UP] and not (snake.direction == 'UP' or
                                                  snake.direction == 'DOWN'):
                        snake.direction = 'UP'
                        snake.yVel -= 10
                        snake.xVel = 0
                    elif keys[pygame.K_DOWN] and not (snake.direction == 'DOWN' or
                                                      snake.direction == 'UP'):
                        snake.direction = 'DOWN'
                        snake.yVel += 10
                        snake.xVel = 0
                    elif keys[pygame.K_LEFT] and not (snake.direction == 'LEFT' or
                                                      snake.direction == 'RIGHT'):
                        snake.direction = 'LEFT'
                        snake.xVel -= 10
                        snake.yVel = 0
                    elif keys[pygame.K_RIGHT] and not (snake.direction == 'RIGHT' or
                                                       snake.direction == 'LEFT'):
                        snake.direction = 'RIGHT'
                        snake.xVel += 10
                        snake.yVel = 0

            snake.snake_move()
            if self.check_collisions(snake, food):
                self.game_over_screen(snake)
            else:
                self.update_window(snake, food)
            clock.tick(10)

if __name__ == "__main__":
    game1 = Game()
    game1.game_init()
