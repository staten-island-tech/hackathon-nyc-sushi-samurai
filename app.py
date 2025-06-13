import pygame
import random
import sys
import json
import os

pygame.init()

# Screen setup
scene1_bg = pygame.image.load('background.jpg')
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt ( New York Edition )")

# Clock
clock = pygame.time.Clock()

# Load images
duck_image_right = pygame.transform.scale(pygame.image.load("pigeon.png"), (80, 80))
duck_image_left = pygame.transform.scale(pygame.image.load("fpigeon.png"), (80, 80))
rat_image_right = pygame.transform.scale(pygame.image.load("rat.png"), (60, 60))
rat_image_left = pygame.transform.scale(pygame.image.load("frat.png"), (60, 60))

# Fonts
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Leaderboard file path
LEADERBOARD_FILE = "leaderboard.json"

# Load leaderboard from file
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)  # list of [name, score]
    return []

# Save leaderboard to file
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

# Game state
game_started = False
name_input_active = False
player_name = ""
show_tips = False
show_leaderboard = False
game_over = False
score_added_to_leaderboard = False

leaderboard = load_leaderboard()  # Now loaded from file

# Buttons
button_width, button_height = 200, 80
start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)
tips_button = pygame.Rect(WIDTH // 2 - button_width // 2, start_button.y + 100, button_width, button_height)
leaderboard_button = pygame.Rect(WIDTH // 2 - button_width // 2, tips_button.y + 100, button_width, button_height)
back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 60)
back_to_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

# Game variables
bullets = 10
score = 0
bonus_score = 0
last_bonus_score = -1
bonus_active = False
bonus_timer = 0
bonus_text = ""
BONUS_DURATION = 60
start_time = pygame.time.get_ticks()

# Reset game function
def reset_game():
    global bullets, score, bonus_score, last_bonus_score, bonus_active, bonus_timer
    global bonus_text, game_over, start_time, ducks, rats, score_added_to_leaderboard

    bullets = 10
    score = 0
    bonus_score = 0
    last_bonus_score = -1
    bonus_active = False
    bonus_timer = 0
    bonus_text = ""
    game_over = False
    score_added_to_leaderboard = False
    start_time = pygame.time.get_ticks()
    ducks.empty()
    rats.empty()

# Duck class
class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = random.choice(["left", "right"])
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 1000
        base_speed = 2
        speed_increase = elapsed_seconds * 0.05
        final_speed = min(base_speed + speed_increase, 5)

        if self.direction == "right":
            self.image = duck_image_right
            self.rect = self.image.get_rect()
            self.rect.x = -self.rect.width
            self.speed = random.uniform(final_speed, final_speed + 1.5)
        else:
            self.image = duck_image_left
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.speed = -random.uniform(final_speed, final_speed + 1.5)

        self.rect.y = random.randint(50, HEIGHT - 150)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Rat class
class Rat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = random.choice(["left", "right"])
        if self.direction == "right":
            self.image = rat_image_right
            self.rect = self.image.get_rect()
            self.rect.x = -self.rect.width
            self.speed = random.uniform(8, 10)
        else:
            self.image = rat_image_left
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.speed = -random.uniform(8, 10)

        self.rect.y = HEIGHT - 100

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Sprite groups
ducks = pygame.sprite.Group()
rats = pygame.sprite.Group()

# Timers
SPAWN_EVENT = pygame.USEREVENT + 1
RAT_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVENT, 1500)
pygame.time.set_timer(RAT_SPAWN_EVENT, 8000)

# Main loop
running = True
while running:
    screen.blit(scene1_bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    reset_game()
                elif back_to_menu_button.collidepoint(event.pos):
                    reset_game()
                    game_started = False
                    name_input_active = False
                    show_tips = False
                    show_leaderboard = False
        elif not game_started:
            if name_input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        name_input_active = False
                        game_started = True
                        start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 12:
                            player_name += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if show_tips:
                        if back_button.collidepoint(event.pos):
                            show_tips = False
                    elif show_leaderboard:
                        show_leaderboard = False
                    elif start_button.collidepoint(event.pos):
                        name_input_active = True
                        player_name = ""
                    elif tips_button.collidepoint(event.pos):
                        show_tips = True
                    elif leaderboard_button.collidepoint(event.pos):
                        show_leaderboard = True
        else:
            if event.type == SPAWN_EVENT:
                ducks.add(Duck())
            elif event.type == RAT_SPAWN_EVENT:
                rats.add(Rat())
            elif event.type == pygame.MOUSEBUTTONDOWN and bullets > 0:
                mouse_pos = event.pos
                hit = False
                for duck in ducks:
                    if duck.rect.collidepoint(mouse_pos):
                        duck.kill()
                        bullets -= 1
                        score += 1
                        bonus_score += 1
                        hit = True
                        break
                for rat in rats:
                    if rat.rect.collidepoint(mouse_pos):
                        rat.kill()
                        bullets += 5
                        score += 3
                        bonus_text = "RAT BONUS +3!"
                        bonus_active = True
                        bonus_timer = BONUS_DURATION
                        hit = True
                        break
                if not hit:
                    bullets -= 1
                    bonus_active = False
                    bonus_text = ""
                    bonus_timer = 0
                    bonus_score = 0

    # Draw UI
    if game_over:
        screen.blit(scene1_bg, (0, 0))
        color = (255, 0, 0)
        final_text = large_font.render(f"Final Score: {score}", True, color)
        screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2 - 60))
        pygame.draw.rect(screen, (0, 150, 0), play_again_button)
        again_text = font.render("Play Again", True, (255, 255, 255))
        screen.blit(again_text, (play_again_button.centerx - again_text.get_width() // 2, play_again_button.centery - 15))
        pygame.draw.rect(screen, (100, 0, 0), back_to_menu_button)
        menu_text = font.render("Back to Menu", True, (255, 255, 255))
        screen.blit(menu_text, (back_to_menu_button.centerx - menu_text.get_width() // 2, back_to_menu_button.centery - 15))

    elif not game_started:
        if name_input_active:
            prompt_text = font.render("Enter Your Name:", True, (0, 0, 0))
            name_surface = font.render(player_name + "|", True, (0, 0, 128))
            screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, HEIGHT // 2))
        elif show_tips:
            tip_lines = [
                "TIPS:",
                "- Click pigeons to score points.",
                "- Click rats for bullets + bonus points!",
                "- Missing costs a bullet!",
                "- 5 pigeon hits = BONUS!",
                "- GO FOR STREAKS!!"
            ]
            for i, line in enumerate(tip_lines):
                tip_text = font.render(line, True, (0, 0, 0))
                screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, 100 + i * 40))
            pygame.draw.rect(screen, (200, 0, 0), back_button)
            back_text = font.render("Back", True, (255, 255, 255))
            screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - 15))
        elif show_leaderboard:
            title_text = font.render("LEADERBOARD", True, (0, 0, 128))
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))
            if leaderboard:
                for i, (name, score_val) in enumerate(leaderboard):
                    entry = f"{i+1}. {name} - {score_val}"
                    lb_text = font.render(entry, True, (0, 0, 128))
                    screen.blit(lb_text, (WIDTH // 2 - lb_text.get_width() // 2, 130 + i * 40))
            else:
                empty_text = font.render("No scores yet!", True, (150, 0, 0))
                screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, 150))

            back_text = font.render("Click anywhere to go back", True, (200, 0, 0))
            screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 60))
        else:
            pygame.draw.rect(screen, (0, 200, 0), start_button)
            pygame.draw.rect(screen, (0, 150, 150), tips_button)
            pygame.draw.rect(screen, (150, 0, 150), leaderboard_button)
            screen.blit(font.render("START GAME", True, (255, 255, 255)), (start_button.centerx - 80, start_button.centery - 20))
            screen.blit(font.render("TIPS", True, (255, 255, 255)), (tips_button.centerx - 30, tips_button.centery - 20))
            screen.blit(font.render("LEADERBOARD", True, (255, 255, 255)), (leaderboard_button.centerx - 90, leaderboard_button.centery - 20))
    else:
        if bonus_score != 0 and bonus_score % 5 == 0 and score != last_bonus_score:
            score += 2
            bullets = min(bullets + random.randint(6, 7), 10)
            bonus_active = True
            bonus_timer = BONUS_DURATION
            bonus_text = "BONUS +2!"
            last_bonus_score = score
            bonus_score = 0

        ducks.update()
        rats.update()
        ducks.draw(screen)
        rats.draw(screen)
        screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Bullets: {bullets}", True, (0, 0, 0)), (10, 40))

        if bonus_active:
            bonus_surface = font.render(bonus_text, True, (255, 0, 0))
            screen.blit(bonus_surface, (WIDTH // 2 - bonus_surface.get_width() // 2, 50))
            bonus_timer -= 1
            if bonus_timer <= 0:
                bonus_active = False
                bonus_text = ""

        if bullets <= 0 and not game_over:
            game_over = True
            if player_name.strip() and not score_added_to_leaderboard:
                leaderboard.append([player_name.strip(), score])
                leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]
                save_leaderboard(leaderboard)
                score_added_to_leaderboard = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
