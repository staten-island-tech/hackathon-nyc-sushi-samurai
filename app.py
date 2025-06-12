import pygame
import random
import sys

pygame.init()


scene1_bg = pygame.image.load('background.jpg')

# Screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt ( New York Edition )")

# Clock
clock = pygame.time.Clock()

# Load duck image
duck_image = pygame.image.load("pigeon.png")
duck_image = pygame.transform.scale(duck_image, (80, 80))

# Font
font = pygame.font.SysFont(None, 36)

# Score
score = 0

# Duck class
class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = duck_image
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width  # Start off screen
        self.rect.y = random.randint(50, HEIGHT - 150)
        self.speed = random.randint(30, 50)

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()  # Remove duck if it leaves screen

# Sprite group for ducks
ducks = pygame.sprite.Group()

# Spawn timer
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

# Main loop
running = True
while running:
    screen.blit(scene1_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT:
            ducks.add(Duck())

        if event.type == pygame.MOUSEBUTTONDOWN:
            for duck in ducks:
                if duck.rect.collidepoint(event.pos):
                    duck.kill()
                    score += 1

    ducks.update()
    ducks.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()