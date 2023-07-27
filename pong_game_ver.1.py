import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta layar
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ukuran bola dan pemain
BALL_SIZE = 20
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 100

# Kecepatan pemain dan bola
PLAYER_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
COMPUTER_SPEED = 4  # Kecepatan komputer

# Fungsi untuk menggambar pemain
def draw_player(surface, x, y):
    pygame.draw.rect(surface, WHITE, pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT))

# Fungsi untuk menggambar bola
def draw_ball(surface, x, y):
    pygame.draw.circle(surface, WHITE, (x, y), BALL_SIZE)

# Fungsi untuk menggambar start screen
def draw_start_screen(surface, font):
    surface.fill(BLACK)

    # Gambar "Pong Game" dengan teks dempet
    game_title_text = font.render("Pong Game", True, WHITE)
    game_title_x = (SCREEN_WIDTH - game_title_text.get_width()) // 2
    game_title_y = (SCREEN_HEIGHT - game_title_text.get_height()) // 2 - 100
    surface.blit(game_title_text, (game_title_x, game_title_y))

    # Gambar "Made by Domas" dengan teks dempet
    made_by_text = font.render("Made by Domas", True, WHITE)
    made_by_x = (SCREEN_WIDTH - made_by_text.get_width()) // 2
    made_by_y = (SCREEN_HEIGHT - made_by_text.get_height()) // 2 - 50
    surface.blit(made_by_text, (made_by_x, made_by_y))

    # Gambar tombol 1 Player vs Computer (Normal)
    normal_button = pygame.Rect((SCREEN_WIDTH - 250) // 2, SCREEN_HEIGHT // 2, 250, 50)
    pygame.draw.rect(surface, WHITE, normal_button)
    normal_text = font.render("vs Computer", True, BLACK)
    surface.blit(normal_text, ((SCREEN_WIDTH - normal_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 10))

    # Gambar tombol Multiplayer
    multiplayer_button = pygame.Rect((SCREEN_WIDTH - 250) // 2, SCREEN_HEIGHT // 2 + 60, 250, 50)
    pygame.draw.rect(surface, WHITE, multiplayer_button)
    multiplayer_text = font.render("Multiplayer", True, BLACK)
    surface.blit(multiplayer_text, ((SCREEN_WIDTH - multiplayer_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 70))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if normal_button.collidepoint(event.pos):
                    return "normal"
                elif multiplayer_button.collidepoint(event.pos):
                    return "multiplayer"

# Fungsi untuk menggambar tabel skor
def draw_score(surface, font, score1, score2):
    score_text = font.render(f'{score1} - {score2}', True, WHITE)
    surface.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 10))

# Fungsi untuk mengontrol pergerakan komputer
def computer_movement(ball_y, computer_y):
    if ball_y < computer_y + PLAYER_HEIGHT // 2:
        return -COMPUTER_SPEED
    elif ball_y > computer_y + PLAYER_HEIGHT // 2:
        return COMPUTER_SPEED
    else:
        return 0

# Main function
def main():
    # Membuat layar
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong Game')

    # Font untuk start screen dan tabel skor
    font = pygame.font.Font(None, 50)

    mode = draw_start_screen(screen, font)

    # Posisi pemain dan bola
    player1_y = (SCREEN_HEIGHT - PLAYER_HEIGHT) // 2
    player2_y = (SCREEN_HEIGHT - PLAYER_HEIGHT) // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2

    # Kecepatan pemain dan bola
    player1_speed = 0
    player2_speed = 0
    ball_speed_x = BALL_SPEED_X
    ball_speed_y = BALL_SPEED_Y

    # Skor pemain
    score1 = 0
    score2 = 0

    clock = pygame.time.Clock()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Mengecek tombol yang ditekan
        keys = pygame.key.get_pressed()
        if mode == "normal":
            # Mode 1 Player vs Computer (Normal)
            if keys[pygame.K_w]:
                player1_speed = -PLAYER_SPEED
            elif keys[pygame.K_s]:
                player1_speed = PLAYER_SPEED
            else:
                player1_speed = 0

            # Kontrol pergerakan komputer dengan interpolasi
            player2_speed = computer_movement(ball_y, player2_y)

        elif mode == "multiplayer":
            # Mode Multiplayer
            if keys[pygame.K_w]:
                player1_speed = -PLAYER_SPEED
            elif keys[pygame.K_s]:
                player1_speed = PLAYER_SPEED
            else:
                player1_speed = 0

            if keys[pygame.K_UP]:
                player2_speed = -PLAYER_SPEED
            elif keys[pygame.K_DOWN]:
                player2_speed = PLAYER_SPEED
            else:
                player2_speed = 0

        # Update posisi pemain
        player1_y += player1_speed
        player2_y += player2_speed

        # Batasi pemain agar tidak keluar dari layar
        player1_y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, player1_y))
        player2_y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, player2_y))

        # Update posisi bola
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bola memantul saat mencapai tepi layar
        if ball_y <= 0 or ball_y >= SCREEN_HEIGHT:
            ball_speed_y = -ball_speed_y

        # Bola bertabrakan dengan pemain
        if ball_x <= PLAYER_WIDTH and player1_y < ball_y < player1_y + PLAYER_HEIGHT:
            ball_speed_x = -ball_speed_x
        elif ball_x >= SCREEN_WIDTH - PLAYER_WIDTH - BALL_SIZE and player2_y < ball_y < player2_y + PLAYER_HEIGHT:
            ball_speed_x = -ball_speed_x

        # Bola keluar dari layar, tambahkan skor dan reset posisi bola
        if ball_x <= 0:
            score2 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_speed_x = -ball_speed_x
            ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
        elif ball_x >= SCREEN_WIDTH:
            score1 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_speed_x = -ball_speed_x
            ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

        # Bersihkan layar
        screen.fill(BLACK)

        # Gambar pemain, bola, dan tabel skor
        draw_player(screen, 10, player1_y)
        if mode == "multiplayer":
            draw_player(screen, SCREEN_WIDTH - PLAYER_WIDTH - 10, player2_y)
        else:
            # Jika mode adalah "1 Player vs Computer", gambar pemain komputer juga
            draw_player(screen, SCREEN_WIDTH - PLAYER_WIDTH - 10, player2_y)
        draw_ball(screen, ball_x, ball_y)
        draw_score(screen, font, score1, score2)

        # Update layar
        pygame.display.flip()

        # Batasi kecepatan frame
        clock.tick(60)

if __name__ == '__main__':
    main()
