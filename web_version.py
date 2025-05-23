# Simplified web-compatible version
import pygame
import random
import math

# Initialize pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Temple Run Web")

# Game variables (2D version for web)
clock = pygame.time.Clock()
FPS = 60
game_speed = 5
score = 0
high_score = 0
game_over = False
paused = False

# Player variables (2D)
player_x = width // 2
player_y = height - 100
player_width = 50
player_height = 80
player_y_velocity = 0
is_jumping = False
gravity = 1
lanes = [width//4, width//2, 3*width//4]
current_lane = 1

# Obstacles and coins (2D)
obstacles = []
coins = []
last_obstacle_time = 0
obstacle_interval = 1500
last_coin_time = 0
coin_interval = 1000

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

def reset_game():
    global player_x, player_y, player_y_velocity, is_jumping, current_lane
    global obstacles, coins, score, game_speed, game_over
    player_x = lanes[current_lane]
    player_y = height - 100
    player_y_velocity = 0
    is_jumping = False
    obstacles = []
    coins = []
    score = 0
    game_speed = 5
    game_over = False

def spawn_obstacle():
    lane = random.choice([0, 1, 2])
    obstacle_type = random.choice(["low", "high"])
    if obstacle_type == "low":
        obstacles.append([lanes[lane], height - 150, 50, 50])
    else:
        obstacles.append([lanes[lane], height - 200, 50, 100])

def spawn_coin():
    lane = random.choice([0, 1, 2])
    height_choice = random.choice([height - 150, height - 200])
    coins.append([lanes[lane], height_choice, 20, 20])

def check_collision(rect1, rect2):
    return (rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1])

def main():
    global current_lane, is_jumping, player_y_velocity, player_y, player_x
    global last_obstacle_time, last_coin_time, score, game_speed, game_over, paused
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and (game_over or paused):
                    reset_game()
                if event.key == pygame.K_SPACE and not is_jumping and not game_over and not paused:
                    is_jumping = True
                    player_y_velocity = -15
                if event.key == pygame.K_LEFT and not game_over and not paused:
                    current_lane = max(0, current_lane - 1)
                if event.key == pygame.K_RIGHT and not game_over and not paused:
                    current_lane = min(2, current_lane + 1)
        
        if not paused and not game_over:
            # Update player position
            target_x = lanes[current_lane]
            player_x += (target_x - player_x) * 0.1
            
            # Handle jumping
            if is_jumping:
                player_y += player_y_velocity
                player_y_velocity += gravity
                if player_y >= height - 100:
                    player_y = height - 100
                    is_jumping = False
                    player_y_velocity = 0
            
            # Spawn obstacles and coins
            if current_time - last_obstacle_time > obstacle_interval:
                spawn_obstacle()
                last_obstacle_time = current_time
                obstacle_interval = max(500, obstacle_interval - 10)
            
            if current_time - last_coin_time > coin_interval:
                spawn_coin()
                last_coin_time = current_time
            
            # Update objects
            for obstacle in obstacles[:]:
                obstacle[0] -= game_speed
                if obstacle[0] < -50:
                    obstacles.remove(obstacle)
                if check_collision([player_x, player_y, player_width, player_height], obstacle):
                    game_over = True
            
            for coin in coins[:]:
                coin[0] -= game_speed
                if coin[0] < -20:
                    coins.remove(coin)
                if check_collision([player_x, player_y, player_width, player_height], coin):
                    coins.remove(coin)
                    score += 10
            
            # Increase score and difficulty
            score += 0.1
            game_speed = 5 + score / 1000
        
        # Drawing
        screen.fill((0, 0, 0))
        
        # Draw ground
        pygame.draw.rect(screen, GRAY, (0, height - 50, width, 50))
        
        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x - player_width//2, player_y - player_height, player_width, player_height))
        
        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle[0] - obstacle[2]//2, obstacle[1] - obstacle[3], obstacle[2], obstacle[3]))
        
        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), coin[2])
        
        # Draw HUD
        font = pygame.font.SysFont('Arial', 32)
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("GAME OVER - Press R to restart", True, RED)
            screen.blit(game_over_text, (width//2 - 200, height//2))
        
        if paused:
            paused_text = font.render("PAUSED - Press P to resume", True, WHITE)
            screen.blit(paused_text, (width//2 - 150, height//2))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()

    # Add to event handling:
if event.type == pygame.FINGERDOWN:
    if event.x * width < width * 0.3:  # Left side
        current_lane = max(0, current_lane - 1)
    elif event.x * width > width * 0.7:  # Right side
        current_lane = min(2, current_lane + 1)
    else:  # Center - jump
        if not is_jumping and not game_over and not paused:
            is_jumping = True
            player_y_velocity = -15