import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oregon Trail (Hood Edition)")

background = pygame.image.load('8-bit.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load character sprite
person = pygame.image.load('pixel-art-student-character-png.webp').convert_alpha()
person = pygame.transform.scale(person, (64, 64))  # Resize if needed
flipped_person = pygame.transform.flip(person, True, False)

# Set initial player position and speed
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
player_vy = 0
gravity = 0.5
jump_strength = -10
on_ground = False
facing_right = True
current_sprite = person

FLOOR_Y = HEIGHT - 150
# Set up clock
clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    clock.tick(60)  # Cap FPS to 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
        if facing_right:
            current_sprite = flipped_person
            facing_right = False
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
        if not facing_right:
            current_sprite = person
            facing_right = True

    # Jumping
    if keys[pygame.K_SPACE] and on_ground:
        player_vy = jump_strength
        on_ground = False

    # Apply gravity
    player_vy += gravity
    player_y += player_vy

    # Check collision with floor
    if player_y >= FLOOR_Y:
        player_y = FLOOR_Y
        player_vy = 0
        on_ground = True
    else:
        on_ground = False

    # Boundary clamping
    player_x = max(0, min(WIDTH - person.get_width(), player_x))

    # Fill background
    win.fill((245, 245, 220))  # Parchment color
    player_x = max(0, min(WIDTH - person.get_width(), player_x))
    player_y = max(0, min(HEIGHT - person.get_height(), player_y))
    # Draw character
    
    win.blit(background, (0, 0))
    win.blit(person, (player_x, player_y))

    # Update display
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()