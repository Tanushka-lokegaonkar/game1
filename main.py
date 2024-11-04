import pygame
import random
import asyncio  # To manage Pygbag async requirements

pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background images
bgimg1 = pygame.transform.scale(pygame.image.load("snake/image1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
bgimg2 = pygame.transform.scale(pygame.image.load("snake/image2.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
bgimg3 = pygame.transform.scale(pygame.image.load("snake/image3.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

# Game settings
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Utility function to display text on the screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

# Function to plot the snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Get and set high score from local storage (browser only)
def get_highscore():
    try:
        # JavaScript interaction to get localStorage high score
        return int(window.localStorage.getItem("highscore") or 0)
    except:
        return 0

def set_highscore(score):
    try:
        # JavaScript interaction to set localStorage high score
        window.localStorage.setItem("highscore", str(score))
    except:
        pass

# Welcome screen
async def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(bgimg1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                await gameloop()
        pygame.display.update()
        await asyncio.sleep(0)  # Allow async processing

# Main game loop
async def gameloop():
    # Game variables
    snake_x, snake_y = 45, 55
    init_velocity = 5
    velocity_x, velocity_y = 0, 0
    snake_size = 10
    snk_list = []
    snk_len = 1
    score = 0
    fps = 60

    # Load high score from local storage
    highscore = get_highscore()

    # Generate initial food position
    food_x = random.randint(20, SCREEN_WIDTH // 2)
    food_y = random.randint(20, SCREEN_HEIGHT // 2)

    exit_game = False
    game_over = False

    while not exit_game:
        if game_over:
            set_highscore(highscore)  # Update high score in local storage
            gameWindow.blit(bgimg3, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    await welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x, velocity_y = init_velocity, 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x, velocity_y = -init_velocity, 0
                    elif event.key == pygame.K_UP:
                        velocity_x, velocity_y = 0, -init_velocity
                    elif event.key == pygame.K_DOWN:
                        velocity_x, velocity_y = 0, init_velocity

            # Update snake position
            snake_x += velocity_x
            snake_y += velocity_y

            # Check for collision with food
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                food_x = random.randint(20, SCREEN_WIDTH // 2)
                food_y = random.randint(20, SCREEN_HEIGHT // 2)
                pygame.mixer.music.load('snake/bonus.wav')
                pygame.mixer.music.play()
                snk_len += 10
                highscore = max(score, highscore)

            # Draw background, score, and high score
            gameWindow.blit(bgimg2, (0, 0))
            text_screen(f"High Score: {highscore}   Score: {score}", WHITE, 5, 5)
            pygame.draw.circle(gameWindow, WHITE, (food_x, food_y), 7)

            # Snake growth and boundary handling
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_len:
                snk_list.pop(0)

            # Check for self-collision or boundary collision
            if head in snk_list[:-1] or not (0 <= snake_x <= SCREEN_WIDTH) or not (0 <= snake_y <= SCREEN_HEIGHT):
                game_over = True
                pygame.mixer.music.load('snake/hit.wav')
                pygame.mixer.music.play()

            # Plot the snake
            plot_snake(gameWindow, RED, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)  # Allow async processing

    pygame.quit()

# Start the game asynchronously
asyncio.run(welcome())
