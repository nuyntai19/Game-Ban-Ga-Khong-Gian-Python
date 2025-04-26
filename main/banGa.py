import pygame as pg 
import random
import menu
from menu import *
# Khởi tạo pygame
pygame.init()
pg.mixer.init()
pg.mixer.music.load("data/nhacnen1.mp3")


# Phát nhạc nền lặp vô hạn
pg.mixer.music.play(-1)

# Cấu hình cửa sổ game
WIDTH, HEIGHT = 1024, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load hình nền
background_img = pygame.image.load("data/bg6.jpg")
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load hình tàu vũ trụ   
ship_img = pygame.image.load("data/phiThuyen2.png")
ship = pygame.transform.scale(ship_img, (50, 50))

# Load hình gà
chicken_img = pygame.image.load("data/ga.png")
chicken_img = pygame.transform.scale(chicken_img, (50, 50))  

# Load hình đạn
bullet_img = pygame.image.load("data/dan.png")
bullet = pygame.transform.scale(bullet_img, (60, 60))

#Load hình cục máu rơi bổ sung cho tàu
heart_img = pygame.image.load("data/mauBoSung.png")
heart_img = pygame.transform.scale(heart_img, (50, 50))

# Đạn của gà
enemy_bullet_img = pygame.image.load("data/dan_ga.png")
enemy_bullet = pygame.transform.scale(enemy_bullet_img, (40, 40))

#Đạn của boss lv 1
boss_bullet_img = pygame.image.load("data/danBossLV1.png")
boss_bullet = pygame.transform.scale(boss_bullet_img, (40, 40))

# vụ nổ khi gà bị bắn
explosion_img = pygame.image.load("data/no.png")
explosion_img = pygame.transform.scale(explosion_img, (50, 50))
explosions = []

# Load hình boss
boss_img = pygame.image.load("data/boss1.png")
boss_img = pygame.transform.scale(boss_img, (100, 100))

# Load hình boss cấp 2
boss_img_lv2 = pygame.image.load("data/boss2.png")
boss_img_lv2 = pygame.transform.scale(boss_img_lv2, (120, 120))

# Load hình boss cấp 3
boss_img_lv3 = pygame.image.load("data/boss3.png")
boss_img_lv3 = pygame.transform.scale(boss_img_lv3, (150, 150))

# Font chữ hiển thị
font = pygame.font.Font(None, 36)

shake_time = 0  # Thời gian rung chấn
shake_intensity = 5  # Cường độ rung (số pixel)

#Biến input
# This dict maps actions to the corresponding key scancodes.
input_map = menu.input_map

# Hàm vẽ nút chơi lại
def draw_restart_button():
    restart_text = FONT.render("REPLAY", True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)) 
    text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, text_rect) # Hiển thị chữ "REPLAY" ở giữa nút chơi lại 
    return pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)

pygame.init()
FONT = pygame.font.Font(None, 40)

BG_COLOR = pygame.Color('gray12') 
GREEN = pygame.Color('lightseagreen')

# Biến để quản lý vị trí của nền
background_y = 0

# Hàm vẽ chữ "Boss Level 1"
def draw_boss_message(screen):
    global boss_message_display_time
    if boss_message_display_time > 0:  # Nếu vẫn còn thời gian hiển thị
        font = pygame.font.Font(None, 74)
        text = font.render("Boss Level 1", True, (255, 0, 0))  # Màu chữ đỏ
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

# Hàm kiểm tra rung chấn
def apply_screen_shake(screen):
    global shake_time, shake_intensity  # Khai báo biến toàn cục
    if shake_time > 0:
        shake_offset_x = random.randint(-shake_intensity, shake_intensity)
        shake_offset_y = random.randint(-shake_intensity, shake_intensity)
        # Dịch chuyển màn hình
        screen.blit(background, (shake_offset_x, shake_offset_y))  # background là hình nền của bạn
        shake_time -= 1  # Giảm thời gian rung chấn
    else:
        # Khi hết rung chấn, hiển thị màn hình bình thường
        screen.blit(background, (0, 0))

def run_game(input_map1=input_map):
    global chicken, background_y, background, shake_time, last_update_time, boss_message_display_time
    # Reset các biến game
    ship_x, ship_y = WIDTH // 2, HEIGHT - 100
    ship_speed = 4
    ship_health = 100
    boss_message_display_time = 3000  # Hiển thị chữ "Boss Level 1" trong 3 giây
    last_update_time = pygame.time.get_ticks()
    chickens = [[random.randint(0, WIDTH - 64), -random.randint(50, 300)] for _ in range(5)]
    chicken_speed = 0.5 # Tốc độ di chuyển của gà

    hearts = []
    heart_speed = 1

    heart_spawn_delay = random.randint(15000, 20000)  
    last_heart_spawn_time = pygame.time.get_ticks() 
    
    # Đạn của tàu và gà 
    bullets = []
    enemy_bullets = []

    # Đạn của boss
    boss_bullets = []

    fire_delay = 250 # Tốc độ bắn của tàu
    last_shot_time = 0

    enemy_fire_delay = 1010  # tốc độ bắn của gà
    last_enemy_shot_time = pygame.time.get_ticks()

    boss_bullet_delay = 600 # Tốc độ bắn của boss
    last_boss_bullet_time = pygame.time.get_ticks()

    score = 0 # Điểm số
    boss = None
    boss_img = None
    boss_health = 300
    boss1_chet = False
    running = True
    game_over = False

    boss_level = 1
    boss_respawn_time = None

    pending_boss_spawn = False  # Cờ chờ xuất hiện boss level 1 sau rung chấn


    
    # Khởi tạo các biến
    
    boss_message_display_time = 0  # Thời gian hiển thị chữ "Boss Level 1"
    boss_message_duration = 3000  # Thời gian hiển thị (3 giây)
    boss_message_shown = False  # Cờ để kiểm soát việc đã hiển thị thông báo chưa

    clock = pygame.time.Clock()

    while running:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_update_time
        last_update_time = current_time

        # Di chuyển nền
        background_y += 0.5
        if background_y >= HEIGHT:
            background_y = 0

        # Áp dụng rung chấn (nếu có)
        if shake_time > 0:
            apply_screen_shake(screen)
        else:
            screen.blit(background, (0, background_y))
            screen.blit(background, (0, background_y - HEIGHT))

        # Hiển thị chữ "Boss Level 1" (nếu cần)
        if boss_message_display_time > 0:
            draw_boss_message(screen)
            boss_message_display_time -= delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Enter the key assignment menu.
                    input_map1 = assignment_menu(input_map1)
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    game_over = False  # Đặt lại trạng thái game
                    run_game()  # Chạy lại game

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    game_over = False
                    run_game()
                    continue

        if not game_over:
            # Điều khiển tàu vũ trụ
            keys = pygame.key.get_pressed()
            if keys[input_map1['move right']] and ship_x < WIDTH - ship.get_width():
                ship_x += ship_speed
            if keys[input_map1['move left']] and ship_x > 0:
                ship_x -= ship_speed
            if keys[input_map1['move up']] and ship_y > 200:
                ship_y -= ship_speed
            if keys[input_map1['move down']] and ship_y < HEIGHT - ship.get_height():
                ship_y += ship_speed

            if keys[input_map1['shoot']]:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time > fire_delay:
                    if boss_level >= 2 :  # Nếu boss đạt cấp 2 thì bắn 3 viên 
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 - 18, ship_y - 40])  # Đạn trái
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2, ship_y - 40])      # Đạn giữa
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 + 18, ship_y - 40])  # Đạn phải
                    else:  # Nếu chưa có boss lv2 thì bắn 1 viên bình thường
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2-2, ship_y - 40])
                    last_shot_time = current_time


            # Di chuyển gà
            for i in range(len(chickens)):
                chickens[i][1] += chicken_speed
                if chickens[i][1] > HEIGHT:
                    chickens[i] = [random.randint(0, WIDTH - 64), -random.randint(50, 300)]

            # Cục máu rơi bổ sung cho tàu
            for i in range(len(hearts)):
                hearts[i][1] += heart_speed
                if hearts[i][1] > HEIGHT:
                    hearts[i] = [random.randint(0, WIDTH - 64), -random.randint(50, 300)]

            # Boss bắn đạn
            if boss and current_time - last_boss_bullet_time > boss_bullet_delay:
                if boss_level >= 2:  # Khi boss đạt cấp 2, bắn 3 viên theo góc (-20, 0, 20)
                    for angle in [-20, 0, 20]:  
                        boss_bullets.append([
                            boss[0] + boss_img.get_width() // 2 - boss_bullet_img.get_width() // 2, 
                            boss[1] + boss_img.get_height(), 
                            angle
                        ])
                else:  # Khi boss chưa lên cấp 2, chỉ bắn 1 viên thẳng
                    boss_bullets.append([
                        boss[0] + boss_img.get_width() // 2 - boss_bullet_img.get_width() // 2, 
                        boss[1] + boss_img.get_height(), 
                        0  # Góc 0 độ (bắn thẳng)
                    ])
                
                last_boss_bullet_time = current_time

            # Gà bắn đạn
            current_time = pygame.time.get_ticks()
            visible_chickens = []  # Khởi tạo danh sách rỗng để tránh lỗi UnboundLocalError

            if current_time - last_enemy_shot_time > enemy_fire_delay and chickens:
                visible_chickens = [c for c in chickens if c[1] > 0]  # Chỉ chọn gà đã xuất hiện

                if visible_chickens:  # Kiểm tra danh sách có phần tử không
                    chicken = random.choice(visible_chickens)
                    enemy_bullets.append([
                        chicken[0] + chicken_img.get_width() // 2 - enemy_bullet.get_width() // 2, 
                        chicken[1] + chicken_img.get_height()
                    ])
                    last_enemy_shot_time = current_time

            # Tạo cục máu rơi bổ sung cho tàu
            # Kiểm tra nếu đã đủ thời gian để tạo cục máu mới
            current_time = pygame.time.get_ticks()
            if current_time - last_heart_spawn_time > heart_spawn_delay:
                hearts.append([random.randint(0, WIDTH - 64), -random.randint(50, 300)])
                last_heart_spawn_time = current_time  # Reset bộ đếm thời gian
                
                # Nếu boss cấp 2 trở lên, giảm thời gian spawn máu
                if boss_level >= 2:
                    heart_spawn_delay = random.randint(10000, 15000)  # 10s - 15s
                else:
                    heart_spawn_delay = random.randint(15000, 20000)  # 15s - 20s (bình thường)



            # Di chuyển đạn của tàu
            for b in bullets[:]:
                b[1] -= 4 # Điều chỉnh tốc độ bắn (giảm: thì giảm tốc độ bắn , tăng: thì tăng tốc độ bắn) 
                if b[1] < 0:
                    bullets.remove(b)

            # Di chuyển đạn của gà 
            for eb in enemy_bullets[:]:
                eb[1] += 2  # Điều chỉnh tốc độ bắn ( giảm: thì giảm tốc độ bắn , tăng: thì tăng tốc độ bắn)
                if eb[1] > HEIGHT:
                    enemy_bullets.remove(eb)

            # Di chuyển đạn của boss
            for bb in boss_bullets[:]:
                bb[1] += 2  # Tốc độ rơi xuống
                bb[0] += int(2 * (bb[2] / 20))  # Điều chỉnh hướng theo góc
                if bb[1] > HEIGHT:
                    boss_bullets.remove(bb)


            # Kiểm tra va chạm giữa tàu và cục máu
            for h in hearts[:]:
                if ((h[0] - ship_x) ** 2 + (h[1] - ship_y) ** 2) ** 0.5 < 40:
                    ship_health = min(ship_health + 10, 100)  # Đảm bảo không vượt 100
                    hearts.remove(h)

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
                        score += 1
                        break

             # Kiểm tra va chạm giữa đạn của tàu và boss 
            if boss is not None and isinstance(boss, list) and len(boss) >= 2:
                for b in bullets[:]:
                    if isinstance(b, list) and len(b) >= 2:
                        if boss is not None and ((boss[0] - b[0]) ** 2 + (boss[1] - b[1]) ** 2) ** 0.5 < 50:
                            bullets.remove(b)
                            boss_health -= 10
                            if boss_health <= 0:
                                print(f"🔥 Boss {boss_level} bị tiêu diệt, đặt boss = None")
                                boss = None  # Xóa boss lv1
                                boss_speed = 0  # Đặt lại tốc độ của boss
                                boss_health = 0  # Đặt lại máu của boss
                                boss_level = 2
                                boss_respawn_time = pygame.time.get_ticks()  # Đặt thời gian hồi sinh cho boss lv2
                                print(f"⏳ Boss lv2 sẽ hồi sinh sau 3s. boss_respawn_time = {boss_respawn_time}")
            # Kiểm tra nếu đạt điểm để xuất hiện boss cấp 1
            # Khi đủ điểm, khởi động rung chấn và hiển thị chữ — chưa tạo boss
            if score >= 5 and boss is None and boss_level == 1 and not pending_boss_spawn:
                shake_time = 90  # Rung chấn ~1.5 giây nếu 60 FPS
                boss_message_display_time = 1500  # Hiển thị chữ 1.5 giây (cùng thời gian rung)
                pending_boss_spawn = True  # Đánh dấu chuẩn bị xuất hiện boss

            # Khi rung chấn kết thúc, mới tạo boss
            if pending_boss_spawn and shake_time == 0 and boss is None and boss_level == 1:
                boss = [WIDTH // 2 - 50, 50]
                boss_speed = 0.8
                boss_img = pygame.image.load("data/boss1.png")
                boss_img = pygame.transform.scale(boss_img, (100, 100))
                boss_health = 300

                # Đổi nhạc nền khi boss xuất hiện
                pg.mixer.music.stop()
                pg.mixer.music.load("data/nhacnen2.mp3")
                pg.mixer.music.play(-1)

                boss1_chet = False
                pending_boss_spawn = False  # Reset cờ

            if boss is not None and boss_level == 1 and boss_health <= 0:
                            if not boss1_chet:  # Chỉ đổi nhạc lần đầu khi boss chết
                                # Đổi lại nhạc nền khi boss lv1 chết
                                pg.mixer.music.stop()
                                pg.mixer.music.load("data/nhacnen1.mp3")
                                pg.mixer.music.play(-1)
                                boss1_chet = True
                            
                            boss = None  # reset boss
                            boss_level = 2  # Chuẩn bị cho boss level 2
                            boss_respawn_time = pygame.time.get_ticks() 

             # Đặt thời gian hồi sinh cho boss lv2
            # Xuất hiện boss lv2 khi tiêu diệt thêm 20 con gà (score đạt 40)
            # Xuất hiện boss lv2 sau khi boss lv1 bị tiêu diệt 3 giây
            if boss is None and boss_respawn_time is not None:
                elapsed_time = pygame.time.get_ticks() - boss_respawn_time
                print(f"⏳ Đã chờ {elapsed_time} ms để hồi sinh boss lv2")
                
                if score >= 30:
                    if elapsed_time > 3000 :  
                        print("🔥 Hồi sinh boss lv2!")
                        boss = [WIDTH // 2 - 60, 50]
                        boss_speed = 0.4
                        boss_img = boss_img_lv2
                        boss_health = 400
                        boss_level = 3
                        boss_bullet_delay = 1000  # Giảm thời gian bắn
            # Kiểm tra va chạm giữa đạn của boss và tàu
            for bb in boss_bullets[:]:
                if ((bb[0] - ship_x) ** 2 + (bb[1] - ship_y) ** 2) ** 0.5 < 40:
                    ship_health -= 20  # Boss gây sát thương cao hơn
                    boss_bullets.remove(bb)

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

        
            # Hiển thị đạn của boss
            for bb in boss_bullets:
                screen.blit(boss_bullet_img, (bb[0], bb[1]))

            
            if boss:
                boss[0] += boss_speed
                if boss[0] <= 0 or boss[0] >= WIDTH - boss_img.get_width():
                    boss_speed = -boss_speed
                
                if boss_level == 1:
                    screen.blit(boss_img, (boss[0], boss[1]))
                else:
                    screen.blit(boss_img_lv2, (boss[0], boss[1]))


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

            for h in hearts:
                screen.blit(heart_img, (h[0], h[1]))

            score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (WIDTH - 125, 10)) 

            # Hiển thị thanh máu
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, ship_health * 2, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20), 2)
        else:
            # Hiển thị màn hình Game Over
            game_over_text = FONT.render("GAME OVER!", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
            restart_button = draw_restart_button()  # Vẽ nút chơi lại
        clock.tick(60) 
        pygame.display.update()
        
# Main menu function
def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        # Draw title
        screen.blit(BG, (0, 0))
        screen.blit(text, textRect)

        update_buttons(buttons)
        draw_buttons(buttons)

        start_button = buttons[0]
        option_button = buttons[1]
        quit_button = buttons[2]

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    print("Game Starting...") 
                    return run_game()
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if option_button.rect.collidepoint(event.pos):
                    options()  # Open options menu
if __name__ == '__main__':
    main_menu()