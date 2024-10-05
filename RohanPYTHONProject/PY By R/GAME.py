import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Obstacles and Score")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Player properties
player_width, player_height = 50, 50
player_x, player_y = 100, HEIGHT - player_height - 60
player_velocity_x, player_velocity_y = 0, 0
player_speed = 5
gravity = 0.5
jump_strength = 10
is_jumping = False
player_lives = 3

# Platform properties
platform_width, platform_height = 200, 20
platform_x, platform_y = 150, HEIGHT - 100

# Enemy properties
enemy_width, enemy_height = 50, 50
enemy_x, enemy_y = 500, HEIGHT - enemy_height - 60
enemy_speed = 3
enemy_direction = 1  # 1 for right, -1 for left
enemy_patrol_range = 150
enemy_start_x = enemy_x
enemy_shoot_cooldown = 1000  # milliseconds between shots
last_shot_time = 0  # Track when the last shot was fired

# Bullet properties (enemy and player)
enemy_bullets = []
player_bullets = []
bullet_speed = 7
bullet_width, bullet_height = 10, 5

# Score tracking
score = 0

# Font for displaying score
font = pygame.font.SysFont("Arial", 30)

# Obstacles (array of dictionaries for size and position)
obstacles = [
    {"x": 300, "y": HEIGHT - 150, "width": 50, "height": 50},  # Obstacle 1
    {"x": 400, "y": HEIGHT - 200, "width": 100, "height": 50},  # Obstacle 2
    {"x": 550, "y": HEIGHT - 100, "width": 75, "height": 75}   # Obstacle 3
]

# Main game loop
def game_loop():
    global player_x, player_y, player_velocity_x, player_velocity_y, is_jumping, player_lives, enemy_y
    global enemy_x, enemy_direction, last_shot_time, score

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_velocity_x = -player_speed
        elif keys[pygame.K_RIGHT]:
            player_velocity_x = player_speed
        else:
            player_velocity_x = 0

        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = -jump_strength
            is_jumping = True

        # Player shoots using the 'S' key
        if keys[pygame.K_s]:
            bullet_x = player_x + player_width // 2
            bullet_y = player_y + player_height // 2
            player_bullets.append([bullet_x, bullet_y])

        # Apply gravity
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Update player position
        player_x += player_velocity_x

        # Collision detection for the player and the platform
        if (platform_x < player_x < platform_x + platform_width or
            platform_x < player_x + player_width < platform_x + platform_width):
            if platform_y < player_y + player_height < platform_y + platform_height:
                player_y = platform_y - player_height
                player_velocity_y = 0
                is_jumping = False

        # Player collision with the ground
        if player_y + player_height >= HEIGHT:
            player_y = HEIGHT - player_height
            player_velocity_y = 0
            is_jumping = False

        # Enemy patrol movement (left-right)
        enemy_x += enemy_direction * enemy_speed
        if abs(enemy_x - enemy_start_x) > enemy_patrol_range:
            enemy_direction *= -1  # Reverse direction when reaching patrol limit

        # Enemy shooting logic
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > enemy_shoot_cooldown:
            last_shot_time = current_time
            bullet_x = enemy_x + enemy_width // 2
            bullet_y = enemy_y + enemy_height // 2
            enemy_bullets.append([bullet_x, bullet_y])

        # Update enemy bullets
        for bullet in enemy_bullets[:]:
            bullet[0] -= bullet_speed  # Move the bullet to the left
            if bullet[0] < 0:
                enemy_bullets.remove(bullet)  # Remove bullets that are off-screen

        # Update player bullets
        for bullet in player_bullets[:]:
            bullet[0] += bullet_speed  # Move the bullet to the right
            if bullet[0] > WIDTH:
                player_bullets.remove(bullet)  # Remove bullets that are off-screen

        # Check for bullet collisions with the player
        for bullet in enemy_bullets[:]:
            if (player_x < bullet[0] < player_x + player_width and
                player_y < bullet[1] < player_y + player_height):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                print(f"Player hit! Lives remaining: {player_lives}")
                if player_lives <= 0:
                    print("Game Over")
                    pygame.quit()
                    sys.exit()

        # Check for player bullet collisions with the enemy
        for bullet in player_bullets[:]:
            if (enemy_x < bullet[0] < enemy_x + enemy_width and
                enemy_y < bullet[1] < enemy_y + enemy_height):
                player_bullets.remove(bullet)
                print("Enemy hit!")
                score += 10  # Increase score by 10 when enemy is hit
                # Reset enemy position or respawn
                enemy_x, enemy_y = random.randint(600, 750), HEIGHT - enemy_height - 60

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))  # Player
        pygame.draw.rect(screen, GREEN, (platform_x, platform_y, platform_width, platform_height))  # Platform
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))  # Enemy

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, ORANGE, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

            # Check for player collisions with obstacles
            if (obstacle["x"] < player_x < obstacle["x"] + obstacle["width"] or
                obstacle["x"] < player_x + player_width < obstacle["x"] + obstacle["width"]):
                if obstacle["y"] < player_y + player_height < obstacle["y"] + obstacle["height"]:
                    player_y = obstacle["y"] - player_height
                    player_velocity_y = 0
                    is_jumping = False

        # Draw bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))  # Enemy bullets
        for bullet in player_bullets:
            pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_width, bullet_height))  # Player bullets

        # Display the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Set the FPS
        clock.tick(FPS)

# Start the game
if __name__ == "__main__":
    game_loop()
