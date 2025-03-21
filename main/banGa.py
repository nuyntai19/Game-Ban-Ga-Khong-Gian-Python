import pygame
import random

# Khởi tạo pygame
pygame.init()

# Cấu hình cửa sổ game
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load hình nền
background_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/background2.jpg")
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load hình tàu vũ trụ   
ship_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/phiThuyen2.png")
ship = pygame.transform.scale(ship_img, (50, 50))

# Load hình gà
chicken_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/ga.png")
chicken_img = pygame.transform.scale(chicken_img, (50, 50))  
  
# Load hình đạn
bullet_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/dan.png")
bullet = pygame.transform.scale(bullet_img, (60, 60))

# Đạn của gà
enemy_bullet_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/dan_ga.png")
enemy_bullet = pygame.transform.scale(enemy_bullet_img, (40, 40))

# vụ nổ khi gà bị bắn
explosion_img = pygame.image.load("C:/Users/ACER/OneDrive/game/data/no.png")
explosion_img = pygame.transform.scale(explosion_img, (50, 50))
explosions = []

# Font chữ hiển thị
font = pygame.font.Font(None, 36)

# Hàm vẽ nút chơi lại
def draw_restart_button():
    restart_text = font.render("REPLAY", True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)) 
    text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, text_rect)
    return pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)

# Hàm chạy game
def run_game():  
    global chicken
    # Reset các biến game
    ship_x, ship_y = WIDTH // 2, HEIGHT - 100
    ship_speed = 1
    ship_health = 100

    chickens = [[random.randint(0, WIDTH - 64), -random.randint(50, 300)] for _ in range(5)]
    chicken_speed = 0.15

    bullets = []
    enemy_bullets = []

    fire_delay = 150 # Tốc độ bắn của tàu
    last_shot_time = 0

    enemy_fire_delay = 1000  # Chậm lại tốc độ bắn của gà
    last_enemy_shot_time = pygame.time.get_ticks()

    running = True
    game_over = False

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    return run_game()  # Chơi lại game

        if not game_over:
            # Điều khiển tàu vũ trụ
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and ship_x > 0:
                ship_x -= ship_speed
            if keys[pygame.K_RIGHT] and ship_x < WIDTH - ship.get_width():
                ship_x += ship_speed
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time > fire_delay:
                    bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2, ship_y])
                    last_shot_time = current_time

            # Di chuyển gà
            for i in range(len(chickens)):
                chickens[i][1] += chicken_speed
                if chickens[i][1] > HEIGHT:
                    chickens[i] = [random.randint(0, WIDTH - 64), -random.randint(50, 300)]

            # Gà bắn đạn
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_shot_time > enemy_fire_delay:
                chicken = random.choice(chickens)
                enemy_bullets.append([chicken[0] + chicken_img.get_width() // 2 - enemy_bullet.get_width() // 2, chicken[1] + chicken_img.get_height()])
                last_enemy_shot_time = current_time

            # Di chuyển đạn của tàu
            for b in bullets[:]:
                b[1] -= 3
                if b[1] < 0:
                    bullets.remove(b)

            # Di chuyển đạn của gà (chậm lại)
            for eb in enemy_bullets[:]:
                eb[1] += 0.8 # Tốc độ giảm còn 0.8
                if eb[1] > HEIGHT:
                    enemy_bullets.remove(eb)

            # Kiểm tra va chạm giữa đạn của tàu và gà
            for b in bullets[:]:
                for i in range(len(chickens)):
                    if ((chickens[i][0] - b[0]) ** 2 + (chickens[i][1] - b[1]) ** 2) ** 0.5 < 30:
                        bullets.remove(b)
                        explosions.append([
                            chickens[i][0] + chicken_img.get_width() // 2 - explosion_img.get_width() // 2,
                            chickens[i][1] + chicken_img.get_height() // 2 - explosion_img.get_height() // 2,
                            pygame.time.get_ticks()
                        ])

                        chickens[i] = [random.randint(0, WIDTH - 64), -random.randint(50, 300)]
                        break

            # Hiển thị vụ nổ
            for explosion in explosions[:]:
                screen.blit(explosion_img, (explosion[0], explosion[1]))
                if pygame.time.get_ticks() - explosion[2] > 500:  # Hiển thị trong 500ms
                    explosions.remove(explosion)        

            # Kiểm tra va chạm giữa đạn của gà và tàu
            for eb in enemy_bullets[:]:
                if ((eb[0] - ship_x) ** 2 + (eb[1] - ship_y) ** 2) ** 0.5 < 40:
                    ship_health -= 10
                    enemy_bullets.remove(eb)

            # Kiểm tra Game Over
            if ship_health <= 0:
                game_over = True

        # Vẽ tàu, gà, đạn
        if not game_over:
            screen.blit(ship, (ship_x, ship_y))
            for chicken_x, chicken_y in chickens:
                screen.blit(chicken_img, (chicken_x, chicken_y))
            for b in bullets:
                screen.blit(bullet, (b[0], b[1]))
            for eb in enemy_bullets:
                screen.blit(enemy_bullet, (eb[0], eb[1]))

            # Hiển thị thanh máu
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, ship_health * 2, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20), 2)
        else:
            # Hiển thị màn hình Game Over
            game_over_text = font.render("GAME OVER!", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
            restart_button = draw_restart_button()  # Vẽ nút chơi lại

        pygame.display.update()

run_game()
pygame.quit()
