# Segment is a block of the Snake
# The snake is constructed of these segments
class Segment:
    def __init__(self, x, y, colour, width=10):
        self.x, self.y = x, y
        self.colour = colour
        self.width = width

# Draw the segment at the specified coordinates
# Segments are squares with dimensions of width*width
    def segment_draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width,
                                               self.width), 0)


# Snake class
# Length controls starting number of segments
# self.segments is used to store the segments of the snake
# xVel and yVel are velocities used to determine snake movement
# direction is a label of the current direction of the snake
class Snake:
    def __init__(self, colour, length=5, size=500):
        self.colour = colour
        self.initial_length = length
        self.length = length
        self.segments = []
        self.x, self.y = size//2, size//2
        self.xVel, self.yVel = -10, 0
        self.direction = 'LEFT'
        for i in range(length):
            self.segments.append(Segment(self.x, self.y, colour))
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
        self.segments.insert(0, Segment(self.x, self.y, self.colour))
        self.segments.pop()

# Function to add a new segment to the snake
# Draws a head in the place of the eaten food
    def snake_grow(self):
        self.x += self.xVel
        self.y += self.yVel
        self.segments.insert(0, Segment(self.x, self.y, self.colour))


# Food is the objective that snake is meant to reach
# Food will cause the snake to grow and score to increase
class Food:
    def __init__(self, x=0, y=0, colour=RED, width=10):
        self.x, self.y = x, y
        self.colour = colour
        self.width = width

# Draw the food at the specified coordinates
# Food is a square of width*width dimension
    def food_draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y,
                                               self.width, self.width), 0)

# Update coordinates after the food has been eaten
    def food_new(self):
        self.x = random.choice(range(10, size, self.width))
        self.y = random.choice(range(10, size, self.width))
