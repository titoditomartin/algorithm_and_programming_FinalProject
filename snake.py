import pygame
import sys
import random


class Snake():
    def __init__(self): 
        self.length = 1 
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (0, 0, 0)
        self.score = 0
        # Sets the initial length and position of the snake, 
        # the direction it is facing (randomly chosen from up, down, left, right), 
        # the color, and the score.

    def get_head_position(self): # Returns the position of the head of the snake.
        return self.positions[0]
        

    def turn(self, point): 
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
        # Takes in a point (direction) as input and changes the direction of the snake to that point. 
        # It also checks if the snake is going in the opposite direction before making the turn.

    def move(self): 
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()
        # Updates the position of the snake by moving its head in the direction it is facing. 
        # It also checks if the snake is colliding with its own body. If so, the game resets.

    def reset(self): # Sets the initial position and length of the snake and its score.
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        # Sets the initial position and length of the snake and its score.

    def draw(self,surface): 
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)
        # Draws the snake on the surface (screen) passed as input.

    def handle_keys(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
    # Allows the user to control the snake by using the arrow keys.
    

class Food(): # Creates an object of food that can be displayed on the game screen
    def __init__(self): # Initializes the position, color, and calls the method randomize_position
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self): # Assigns a random position to the food object within the grid
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface): # Creates a rectangle on the surface at the food's position and color,
                             # and also draws a border with a different color
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface): # Creates the game grid on the surface. The grid is drawn as a series of rectangles on the surface
    for y in range(0, int(grid_height)): # iterate over the number of rows
        for x in range(0, int(grid_width)): # iterate over the number of columns
            if (x+y)%2 == 0: # check if the sum of x and y is even
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r) # draw a rectangle on the surface with color (93,216,228)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr) # draw a rectangle on the surface with color (84,194,205)

# Screen size
screen_width = 480
screen_height = 480

# Grid size inside the screen
gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

# The Snake movement across the grids
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init() # Initialize pygame library

    clock = pygame.time.Clock() # Creates a clock object for tracking time
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32) 
    # Sets the screen size and creates a window for the game


    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)
    # Creates a surface and converts it to the appropriate format
    # drawGrid is probably a function that draws the game grid on the surface

    snake = Snake()
    food = Food()
    # Initializes the snake and food objects for the game

    myfont = pygame.font.SysFont("monospace",16) # Creates a font object with the specified font and size

    while (True):
        clock.tick(10) # limit the frame rate to 10 frame per second
        snake.handle_keys() # handle the user input
        drawGrid(surface) # call the method to draw the grid
        snake.move() # move the snake based on its current direction
        if snake.get_head_position() == food.position: # check if the snake's head is on the food
            snake.length += 1 # increase the snake's length
            snake.score += 1 # increase the score
            food.randomize_position() # move the food to a random position
        snake.draw(surface) # draw the snake
        food.draw(surface) # draw the food
        screen.blit(surface, (0,0)) # update the screen 
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0)) # render the score text
        screen.blit(text, (5,10)) # draw the score text on the screen
        pygame.display.update() # update the display

main()
