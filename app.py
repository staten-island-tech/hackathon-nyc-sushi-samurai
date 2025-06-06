import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oregon Trail(Hood Edition)")
person=pygame.image.load('New Piskel.png').convert_alpha()
clock = pygame.time.Clock()
running = True

while running:
    win.fill((245, 245, 220))  # Light parchment background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.blit(person,(100,100))
    
    # Update game logic here
    # Draw UI and assets here

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()