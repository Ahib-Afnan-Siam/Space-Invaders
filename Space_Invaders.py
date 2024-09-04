import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player_width = 50
player_height = 50
player = pygame.Rect(SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - 100, player_width, player_height)
player_speed = 300  # pixels per second
player_lives = 3

# Player bullet
bullet_width = 5
bullet_height = 10
bullet_color = WHITE
bullet_speed = 500  # pixels per second
bullets = []

# Alien
alien_width = 50
alien_height = 50
alien_speed = 100  # pixels per second
aliens = []

# Alien bullet
alien_bullet_width = 5
alien_bullet_height = 10
alien_bullet_color = WHITE
alien_bullet_speed = 200  # pixels per second
alien_bullets = []

# Score
score = 0
font = pygame.font.Font(None, 36)

def spawn_alien():
    x = random.randint(0, SCREEN_WIDTH - alien_width)
    y = random.randint(-500, -alien_height)
    alien = pygame.Rect(x, y, alien_width, alien_height)
    aliens.append(alien)

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_score():
    draw_text("Score: " + str(score), font, WHITE, 10, 10)

def draw_lives():
    draw_text("Lives: " + str(player_lives), font, WHITE, SCREEN_WIDTH - 100, 10)

def draw_player():
    pygame.draw.rect(screen, WHITE, player)

def draw_aliens():
    for alien in aliens:
        pygame.draw.rect(screen, WHITE, alien)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, bullet)

def draw_alien_bullets():
    for bullet in alien_bullets:
        pygame.draw.rect(screen, alien_bullet_color, bullet)

def move_bullets(delta_time):
    for bullet in bullets:
        bullet.y -= bullet_speed * delta_time

def move_alien_bullets(delta_time):
    for bullet in alien_bullets:
        bullet.y += alien_bullet_speed * delta_time

def move_aliens(delta_time):
    global alien_speed
    for alien in aliens:
        alien.y += alien_speed * delta_time

def check_bullet_collision():
    global score
    for bullet in bullets:
        for alien in aliens:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                # Check if score is a multiple of 50 to increase alien speed
                if score % 50 == 0:
                    increase_alien_speed()

def increase_alien_speed():
    global alien_speed
    alien_speed += 10

def check_alien_bullet_collision():
    global player
    for bullet in alien_bullets:
        if bullet.colliderect(player):
            return True
    return False

def check_player_collision():
    global player_lives
    for alien in aliens:
        if alien.colliderect(player):
            player_lives -= 1
            aliens.remove(alien)
            return True
    return False

def check_alien_reached_bottom():
    global player_lives
    for alien in aliens:
        if alien.bottom >= SCREEN_HEIGHT:
            player_lives -= 1
            aliens.remove(alien)
            return True
    return False

def game_over():
    screen.fill(BLACK)
    draw_text("Game Over!", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text("Score: " + str(score), font, WHITE, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Set up a flag to track if space bar is pressed
space_pressed = False

# Initialize player velocity in x direction
player_vel_x = 0

# Game Loop
running = True
clock = pygame.time.Clock()
alien_spawn_timer = 0
while running:
    delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Update player velocity based on key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_vel_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_vel_x += player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_vel_x += player_speed
            if event.key == pygame.K_RIGHT:
                player_vel_x -= player_speed

    # Update player position based on velocity
    player.x += player_vel_x * delta_time

    # Clamp player's x position to stay within the screen boundaries
    player.x = max(0, min(player.x, SCREEN_WIDTH - player_width))

    # Get current key states
    keys = pygame.key.get_pressed()

    # Shoot bullets
    if keys[pygame.K_SPACE] and not space_pressed:
        bullet = pygame.Rect(player.x + player_width // 2 - bullet_width // 2, player.y, bullet_width, bullet_height)
        bullets.append(bullet)
        space_pressed = True
    elif not keys[pygame.K_SPACE]:
        space_pressed = False

    # Spawn aliens
    alien_spawn_timer += delta_time
    if alien_spawn_timer >= 2.0:  # Spawn an alien every 2 seconds
        spawn_alien()
        alien_spawn_timer = 0

    # Move player bullets
    move_bullets(delta_time)

    # Move aliens
    move_aliens(delta_time)

    # Move alien bullets
    move_alien_bullets(delta_time)

    # Check bullet collision with aliens
    check_bullet_collision()

    # Check collision between player and aliens
    if check_player_collision():
        if player_lives == 0:
            game_over()

    # Check for aliens reaching the bottom without being hit
    if check_alien_reached_bottom():
        if player_lives == 0:
            game_over()

    # Draw everything
    draw_score()
    draw_lives()
    draw_player()
    draw_aliens()
    draw_bullets()

    pygame.display.update()

pygame.quit()
sys.exit()