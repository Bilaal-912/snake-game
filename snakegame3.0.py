import pygame
import random

# Initialize Pygame
pygame.init()

# Load background music
pygame.mixer.music.load('naagin.mp3')  # Replace with your music file
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Load sound effects
death_sound = pygame.mixer.Sound('death.mp3')  # Replace with your death sound file
eat_sound = pygame.mixer.Sound('eat.mp3')      # Replace with your eating sound file

# Load background image
background_image = pygame.image.load('starfield.png')  # Replace with your image file

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)     # Color for the snake's head
GREEN = (0, 255, 0)     # Color for the snake's body
BLUE = (50, 153, 213)
GREY = (169, 169, 169)  # Color for obstacles

# Display settings
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Clock to control game speed
clock = pygame.time.Clock()

# Snake settings
snake_block = 10
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the player's score
def display_score(score):
    value = score_font.render(f"Score: {score}", True, BLUE)
    dis.blit(value, [dis_width - 150, 10])

# Function to draw the snake on the screen
def draw_snake(snake_block, snake_list):
    pygame.draw.rect(dis, RED, [snake_list[-1][0], snake_list[-1][1], snake_block, snake_block])
    for segment in snake_list[:-1]:
        pygame.draw.rect(dis, GREEN, [segment[0], segment[1], snake_block, snake_block])

# Function to display messages on the screen
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Function to draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, GREY, [obstacle[0], obstacle[1], snake_block, snake_block])

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    direction = None

    snake_list = []
    length_of_snake = 1

    egg_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    egg_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    score = 0

    obstacles = []  # List to hold obstacle positions
    level = 1

      # Main game loop
    while not game_over:

        while game_close:
            dis.fill(BLACK)
            display_message("You Lost! Press A-Play Again or Q-Quit", RED)
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_a:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'DOWN'

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        
        # Draw the background image
        dis.blit(background_image, (0, 0))  # Draw the background

        # Wrap the snake around the screen for levels 1 and 2
        if level <= 2:
            if x1 >= dis_width:
                x1 = 0
            elif x1 < 0:
                x1 = dis_width - snake_block
            if y1 >= dis_height:
                y1 = 0
            elif y1 < 0:
                y1 = dis_height - snake_block
        else:  # Level 3 has boundaries
            if x1 < 0 or x1 >= dis_width or y1 < 0 or y1 >= dis_height:
                game_close = True

        pygame.draw.rect(dis, YELLOW, [egg_x, egg_y, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if the snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Check collision with obstacles
        for obstacle in obstacles:
            if snake_head == obstacle:
                game_close = True

        draw_snake(snake_block, snake_list)
        draw_obstacles(obstacles)
        display_score(score)

        pygame.display.update()

        # If the snake collects the egg
        if x1 == egg_x and y1 == egg_y:
            egg_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            egg_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

            # Level up
            if score == 10 and level == 1:
                level = 2
                # Add initial obstacles for level 2
                obstacles = [[random.randrange(0, dis_width, snake_block), random.randrange(0, dis_height, snake_block)] for _ in range(5)]
            elif score == 20 and level == 2:
                level = 3
                # Add more obstacles for level 3
                obstacles.extend([[random.randrange(0, dis_width, snake_block), random.randrange(0, dis_height, snake_block)] for _ in range(5)])
        
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
