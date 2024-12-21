import pygame
import random
import sys

# Inicializē Pygame
pygame.init()

# Krāsu definīcijas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Ekrāna izmēri
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Runner")

# FPS kontrole
clock = pygame.time.Clock()
FPS = 60

# Dinas atribūti
DINO_WIDTH = 40
DINO_HEIGHT = 60
dino_x = 50
dino_y = SCREEN_HEIGHT - DINO_HEIGHT - 20
dino_vel_y = 0
is_jumping = False
jump_height = 15

# Skrišanas zeme
GROUND_HEIGHT = SCREEN_HEIGHT - 20
ground = pygame.Rect(0, GROUND_HEIGHT, SCREEN_WIDTH, 20)

# Šķēršļi
obstacle_width = 20
obstacle_height = 40
obstacle_speed = 5
obstacles = []
spawn_obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_obstacle_event, 1500)  # Ģenerē šķēršļus ik pēc 1.5 sekundēm

# Spēles stāvoklis
game_over = False
score = 0
font = pygame.font.SysFont(None, 36)

def draw_dino(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, DINO_WIDTH, DINO_HEIGHT))

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, RED, obstacle)

def display_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH - 150, 10))

def game_loop():
    global dino_y, dino_vel_y, is_jumping, game_over, score

    while True:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not is_jumping:
                        is_jumping = True
                        dino_vel_y = -jump_height
            if event.type == spawn_obstacle_event:
                obstacle_x = SCREEN_WIDTH
                obstacle = pygame.Rect(obstacle_x, GROUND_HEIGHT - obstacle_height, obstacle_width, obstacle_height)
                obstacles.append(obstacle)

        # Dinas kustība
        if is_jumping:
            dino_y += dino_vel_y
            dino_vel_y += 1  # Gravitation effect

            if dino_y >= SCREEN_HEIGHT - DINO_HEIGHT - 20:
                dino_y = SCREEN_HEIGHT - DINO_HEIGHT - 20
                is_jumping = False
                dino_vel_y = 0

        # Šķēršļu kustība
        for obstacle in obstacles[:]:
            obstacle.x -= obstacle_speed
            if obstacle.right < 0:
                obstacles.remove(obstacle)
                score += 1

        # Saskarsme
        dino_rect = pygame.Rect(dino_x, dino_y, DINO_WIDTH, DINO_HEIGHT)
        for obstacle in obstacles:
            if dino_rect.colliderect(obstacle):
                game_over = True

        if game_over:
            game_over_screen(score)
            break

        # Zeme un spēles elementi
        pygame.draw.rect(screen, GRAY, ground)
        draw_dino(dino_x, dino_y)
        for obstacle in obstacles:
            draw_obstacle(obstacle)
        display_score(score)

        pygame.display.flip()

def game_over_screen(final_score):
    while True:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, RED)
        score_text = font.render(f"Your Score: {final_score}", True, BLACK)
        restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restartē spēli
                    st.session_state.board = [''] * 9
                    st.session_state.current_player = 'X'
                    st.session_state.game_over = False
                    st.session_state.winner = None
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    game_loop()
