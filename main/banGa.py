import pygame as pg 
import random
import menu
from menu import *
import math

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
background_img = pygame.image.load("data/bg9.png")
# Tối ưu: Scale background một lần và lưu vào biến
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background.get_rect()

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

# Đạn của boss lv1
boss_bullet_img = pygame.image.load("data/danBossLV1.png")
boss_bullet = pygame.transform.scale(boss_bullet_img, (40, 40))

# Đạn của boss lv3
boss_bullet_img_lv3 = pygame.image.load("data/dan_Boss_LV3.png")
boss_bullet_img_lv3 = pygame.transform.scale(boss_bullet_img_lv3, (150, 150)) 

# vụ nổ khi gà bị bắn
explosion_img = pygame.image.load("data/no.png")
explosion_img = pygame.transform.scale(explosion_img, (50, 50))
explosions = []

# Load hình boss
boss_img = pygame.image.load("data/boss1.png")
boss_img = pygame.transform.scale(boss_img, (100, 140))

# Load hình boss cấp 2
boss_img_lv2 = pygame.image.load("data/boss2.png")
boss_img_lv2 = pygame.transform.scale(boss_img_lv2, (120, 120))

# Load hình boss lv3 (2 trạng thái)
boss_lv3_frames = []
boss_lv3_frames.append(pygame.transform.scale(pygame.image.load("data/boss3_dangThuong.png"), (400, 250)))
boss_lv3_frames.append(pygame.transform.scale(pygame.image.load("data/boss3_dangNangCap.png"), (400, 250)))

# Load hình hộp quà
gift_img = pygame.image.load("data/GIFT.png")
gift_img = pygame.transform.scale(gift_img, (40, 40))

# Font chữ hiển thị
font = pygame.font.Font(None, 36)

shake_time = 0  # Thời gian rung chấn
shake_intensity = 6  # Cường độ rung (số pixel)

# Biến input
input_map = menu.input_map

plasma_beams = []
last_plasma_time = pygame.time.get_ticks()
PLASMA_INTERVAL = 3000  # Giảm từ 5000 xuống 3000 (3 giây bắn lại)

# Thêm biến mới ở đầu file, sau các biến khác
last_burst_time = 0  # Thời điểm bắt đầu bắn liên tiếp
burst_count = 0      # Số viên đạn đã bắn trong đợt
BURST_INTERVAL = 2000  # 2 giây giữa các đợt bắn
BURST_DURATION = 500   # 0.5 giây cho mỗi đợt bắn
BURST_COUNT = 10      # Số viên đạn trong mỗi đợt

# Thêm biến mới ở đầu file
last_inner_cannon_time = 0
INNER_CANNON_INTERVAL = 500  # Giảm từ 1000ms xuống 500ms (0.5 giây)

class PlasmaBeam:
    def __init__(self, x, y, is_left=True):
        self.x = x
        self.y = y
        self.width = 10
        self.height = HEIGHT
        self.color = (0, 255, 255)
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        self.is_left = is_left
        self.last_damage_time = pygame.time.get_ticks()
        self.animation_time = 0
        self.glow_size = 0
        self.glow_direction = 1
        # Giảm góc xéo vào trong
        self.angle = 5 if is_left else -5  # Giảm từ 10 xuống 5 độ
        self.angle_direction = -1 if is_left else 1
        self.angle_speed = 0.15  # Tăng tốc độ quét để bẻ nhanh hơn
        self.curve_start_time = 1000  # Bắt đầu bẻ góc sau 1 giây

    def update(self, boss_x):
        if pygame.time.get_ticks() - self.spawn_time > 3000:  # 3s tồn tại
            self.active = False
        else:
            # Cập nhật vị trí x theo nòng súng
            if self.is_left:
                self.x = boss_x + 98
            else:
                self.x = boss_x + 302
            
            # Cập nhật animation
            self.animation_time = (pygame.time.get_ticks() - self.spawn_time) % 1000
            # Tạo hiệu ứng nhấp nháy
            self.glow_size += 0.2 * self.glow_direction
            if self.glow_size >= 5 or self.glow_size <= 0:
                self.glow_direction *= -1

            # Cập nhật góc quét
            current_time = pygame.time.get_ticks() - self.spawn_time
            if current_time > self.curve_start_time:
                # Bắt đầu bẻ góc sau khi đã bắn thẳng xuống
                self.angle += self.angle_speed * self.angle_direction
                # Tăng khoảng quét ra ngoài
                if self.angle <= -60 or self.angle >= 60:  # Tăng từ 45 lên 60 độ
                    self.angle_direction *= -1

    def draw(self, screen):
        if self.active:
            # Tính toán các điểm cho tia plasma dựa trên góc
            # Không cần cộng thêm 90 độ nữa vì chúng ta đã điều chỉnh góc trong update
            end_x = self.x + math.sin(math.radians(self.angle)) * self.height
            end_y = self.y + math.cos(math.radians(self.angle)) * self.height

            # Vẽ hiệu ứng glow
            for i in range(3):
                glow_width = int(self.width + (self.glow_size * 2))
                alpha = 100 - (i * 30)
                glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                glow_color = (0, 255, 255, alpha)
                
                pygame.draw.line(glow_surface, glow_color, 
                               (int(self.x), int(self.y)), 
                               (int(end_x), int(end_y)), 
                               glow_width)
                screen.blit(glow_surface, (0, 0))

            # Vẽ tia plasma chính
            brightness = 128 + int(127 * math.sin(self.animation_time * 0.01))
            main_color = (0, brightness, brightness)
            pygame.draw.line(screen, main_color, 
                           (int(self.x), int(self.y)), 
                           (int(end_x), int(end_y)), 
                           int(self.width))

            # Thêm các tia sáng ngang
            for i in range(0, int(self.height), 30):
                progress = i / self.height
                spark_x = self.x + math.sin(math.radians(self.angle)) * i
                spark_y = self.y + math.cos(math.radians(self.angle)) * i
                
                spark_length = random.randint(5, 15)
                spark_angle = self.angle + 90  # Tia sáng vuông góc với tia chính
                
                spark_end_x = spark_x + math.sin(math.radians(spark_angle)) * spark_length
                spark_end_y = spark_y + math.cos(math.radians(spark_angle)) * spark_length
                
                spark_color = (0, 255, 255, 150)
                pygame.draw.line(screen, spark_color, 
                               (int(spark_x), int(spark_y)), 
                               (int(spark_end_x), int(spark_end_y)), 
                               2)

    def check_collision(self, ship_x, ship_y, ship_width, ship_height):
        if not self.active:
            return False
        
        # Tạo rect cho tàu
        ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
        
        # Tính toán các điểm của tia plasma
        end_x = self.x + math.sin(math.radians(self.angle)) * self.height
        end_y = self.y + math.cos(math.radians(self.angle)) * self.height
        
        # Kiểm tra va chạm bằng cách tạo một rect bao quanh tia plasma
        beam_rect = pygame.Rect(
            min(self.x, end_x) - self.width//2,
            min(self.y, end_y) - self.width//2,
            abs(end_x - self.x) + self.width,
            abs(end_y - self.y) + self.width
        )
        
        if ship_rect.colliderect(beam_rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_damage_time >= 500:  # Giảm từ 1000 xuống 500ms
                self.last_damage_time = current_time
                return True
        return False

class BossBulletLv1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.angle = 0
        self.rotation_speed = 5
        self.active = True

    def update(self):
        self.y += self.speed
        # Xoay đạn
        self.angle = (self.angle + self.rotation_speed) % 360
        
        # Kiểm tra nếu đạn ra khỏi màn hình
        if self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        if self.active:
            # Xoay đạn
            rotated_bullet = pygame.transform.rotate(boss_bullet, self.angle)
            # Lấy rect của đạn đã xoay để căn giữa
            bullet_rect = rotated_bullet.get_rect(center=(self.x + 20, self.y + 20))
            screen.blit(rotated_bullet, bullet_rect.topleft)

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

# Hàm vẽ chữ cho các boss
def draw_boss_message(screen, boss_level, is_upgrade=False):
    global boss_message_display_time
    if boss_message_display_time > 0:  # Nếu vẫn còn thời gian hiển thị
        # Tạo hiệu ứng nhấp nháy
        alpha = int(255 * (1 + math.sin(pygame.time.get_ticks() * 0.005)) / 2)
        
        # Sử dụng font RetroFont với kích thước nhỏ hơn cho thông báo nâng cấp
        if is_upgrade:
            font = pygame.font.Font("fonts/RetroFont.ttf", 60)  # Giảm kích thước xuống 60
        else:
            font = pygame.font.Font("fonts/RetroFont.ttf", 80)
        
        # Tạo gradient màu
        colors = [
            (255, 0, 0),    # Đỏ
            (255, 165, 0),  # Cam
            (255, 255, 0),  # Vàng
            (0, 255, 0),    # Xanh lá
            (0, 255, 255),  # Cyan
            (0, 0, 255),    # Xanh dương
            (255, 0, 255)   # Tím
        ]
        
        # Tính toán màu dựa trên thời gian
        color_index = (pygame.time.get_ticks() // 100) % len(colors)
        next_color_index = (color_index + 1) % len(colors)
        color_progress = (pygame.time.get_ticks() % 100) / 100
        
        # Lấy màu hiện tại và màu tiếp theo
        current_color = colors[color_index]
        next_color = colors[next_color_index]
        
        # Tính toán màu gradient
        r = int(current_color[0] * (1 - color_progress) + next_color[0] * color_progress)
        g = int(current_color[1] * (1 - color_progress) + next_color[1] * color_progress)
        b = int(current_color[2] * (1 - color_progress) + next_color[2] * color_progress)
        
        # Tạo text dựa trên level và trạng thái nâng cấp
        if is_upgrade:
            text_content = "BOSS LEVEL 3 UPGRADED!"
        else:
            text_content = f"BOSS LEVEL {boss_level}"
            
        # Tạo text với màu gradient
        text = font.render(text_content, True, (r, g, b))
        text.set_alpha(alpha)
        
        # Tính toán vị trí để căn giữa
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Vẽ bóng đổ
        shadow = font.render(text_content, True, (0, 0, 0))
        shadow.set_alpha(alpha // 2)
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 4, HEIGHT // 2 + 4))
        screen.blit(shadow, shadow_rect)
        
        # Vẽ text chính
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
    ship_speed = menu.game_ship_variables["ship_speed"]
    ship_health = menu.game_ship_variables["ship_health"]
    boss_message_display_time = 3000
    last_update_time = pygame.time.get_ticks()
    last_burst_time = pygame.time.get_ticks()
    burst_count = 0
    last_inner_cannon_time = pygame.time.get_ticks()
    damage_flash_time = 0
    last_ship_health = ship_health
    
    # Tối ưu: Thêm giới hạn số lượng đạn
    MAX_BULLETS = 30  # Giảm số lượng đạn tối đa xuống 30
    fire_delay = 300  # Tăng thời gian giữa các lần bắn lên 300ms
    last_shot_time = pygame.time.get_ticks()  # Khởi tạo thời gian bắn đạn cuối cùng

    # Giới hạn số lượng gà bắn đạn
    MAX_ENEMY_BULLETS = 20  # Giới hạn số lượng đạn của gà
    MAX_SHOOTING_CHICKENS = 3  # Số lượng gà tối đa được phép bắn đạn cùng lúc

    # Tối ưu: Tạo surface cho background cuộn
    scroll_surface = pygame.Surface((WIDTH, HEIGHT * 2))
    scroll_surface.blit(background, (0, 0))
    scroll_surface.blit(background, (0, HEIGHT))

    # Thêm biến cho hộp quà và nòng súng
    gifts = []  # Danh sách hộp quà
    gift_speed = 1.5  # Giảm tốc độ rơi từ 3 xuống 1.5
    last_gift_spawn_time = pygame.time.get_ticks()
    gift_spawn_delay = 15000  # 15 giây spawn một hộp quà
    weapon_level = 1  # Cấp độ vũ khí (1-4 nòng)
    gift_rotation = 0  # Góc xoay của hộp quà

    # Thêm biến cho hiệu ứng shader
    ship_trail = []  # Danh sách lưu các vị trí trước đó của tàu
    last_ship_pos = (ship_x, ship_y)  # Vị trí cuối cùng của tàu
    trail_length = 5  # Số lượng vệt sáng theo sau
    chickens = [[random.randint(0, WIDTH - 64), -random.randint(50, 300)] for _ in range(5)]
    chicken_speed = menu.game_enemy_variables["chicken_speed"] # Tốc độ di chuyển của gà

    hearts = []
    heart_speed = menu.game_enemy_variables["heart_speed"]

    heart_spawn_delay = random.randint(15000, 20000)  
    last_heart_spawn_time = pygame.time.get_ticks() 
    
    # Đạn của tàu và gà 
    bullets = []
    enemy_bullets = []

    # Đạn của boss
    boss_bullets = []

    enemy_fire_delay = menu.game_enemy_variables["enemy_fire_delay"]  # tốc độ bắn của gà
    last_enemy_shot_time = pygame.time.get_ticks()

    boss_bullet_delay = menu.game_enemy_variables["boss_bullet_delay"] # Tốc độ bắn của boss
    last_boss_bullet_time = pygame.time.get_ticks()

    score = 0 # Điểm số
    boss = None
    boss_img = None
    boss_health = menu.game_enemy_variables["boss_health"]
    boss1_chet = False
    boss2_chet = False 
    boss_lv3_upgraded = False 
    running = True
    game_over = False

    boss_level = 1
    boss_respawn_time = None

    last_plasma_time = 0

    pending_boss_spawn = False  # Cờ chờ xuất hiện boss level 1 sau rung chấn

    # Khởi tạo các biến
    
    boss_message_display_time = 0  # Thời gian hiển thị chữ "Boss Level 1"
    boss_message_duration = 3000  # Thời gian hiển thị (3 giây)
    current_boss_message = None  # Khởi tạo biến current_boss_message
    showing_upgrade_message = False  # Cờ để kiểm soát việc hiển thị thông báo nâng cấp

    clock = pygame.time.Clock()

    while running:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_update_time
        last_update_time = current_time

        # Di chuyển nền - Tối ưu tốc độ cuộn
        background_y = (background_y + 0.5) % HEIGHT

        # Áp dụng rung chấn (nếu có)
        if shake_time > 0:
            apply_screen_shake(screen)
        else:
            # Tối ưu: Vẽ background một lần
            screen.blit(scroll_surface, (0, -background_y))

        # Hiển thị chữ "Boss Level 1" (nếu cần)
        if boss_message_display_time > 0:
            draw_boss_message(screen, boss_level)
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
            old_x, old_y = ship_x, ship_y  # Lưu vị trí cũ
            if keys[input_map1['Move Right']] and ship_x < WIDTH - ship.get_width():
                ship_x += ship_speed
            if keys[input_map1['Move Left']] and ship_x > 0:
                ship_x -= ship_speed
            if keys[input_map1['Move Up']] and ship_y > 200:
                ship_y -= ship_speed
            if keys[input_map1['Move Down']] and ship_y < HEIGHT - ship.get_height():
                ship_y += ship_speed

            # Cập nhật vệt sáng khi tàu di chuyển
            if (old_x, old_y) != (ship_x, ship_y):  # Nếu tàu di chuyển
                ship_trail.append((ship_x, ship_y))
                if len(ship_trail) > trail_length:
                    ship_trail.pop(0)  # Xóa vị trí cũ nhất

            # Bắn đạn dựa trên cấp độ vũ khí
            if keys[input_map1['Shoot']]:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time > fire_delay and len(bullets) < MAX_BULLETS:
                    if weapon_level == 1:
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2, ship_y - 40])
                    elif weapon_level == 2:
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 - 15, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 + 15, ship_y - 40])
                    elif weapon_level == 3:
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 - 25, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 + 25, ship_y - 40])
                    elif weapon_level == 4:
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 - 35, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 - 15, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 + 15, ship_y - 40])
                        bullets.append([ship_x + ship.get_width() // 2 - bullet.get_width() // 2 + 35, ship_y - 40])
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

            # Kiểm tra va chạm giữa đạn của boss và tàu
            ship_center_x = ship_x + ship.get_width() // 2
            ship_center_y = ship_y + ship.get_height() // 2

            for bb in boss_bullets[:]:
                if isinstance(bb, BossBulletLv1):
                    bb.update()
                    # Kiểm tra va chạm với tàu
                    if ((bb.x - ship_center_x) ** 2 + (bb.y - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 20  # Tăng từ 15 lên 20 cho boss lv1
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        bb.active = False
                    if not bb.active:
                        boss_bullets.remove(bb)
                elif len(bb) == 4 and bb[3] == 2:  # Boss lv2
                    # Di chuyển đạn theo góc
                    bb[1] += 4  # Tăng tốc độ di chuyển xuống
                    bb[0] += math.sin(math.radians(bb[2])) * 2  # Tăng tốc độ di chuyển ngang
                    
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 20  # Tăng từ 15 lên 20 cho boss lv2
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[1] > HEIGHT + 50:
                        boss_bullets.remove(bb)
                elif len(bb) == 5 and bb[4] == 3:  # Boss lv3 thường
                    bb[0] += bb[2]  # vx
                    bb[1] += bb[3]  # vy
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 15  # Giữ nguyên 15 cho boss lv3
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[0] < -50 or bb[0] > WIDTH + 50 or bb[1] < -50 or bb[1] > HEIGHT + 50:
                        boss_bullets.remove(bb)
                elif len(bb) == 6 and bb[4] == 3:  # Boss lv3 nâng cấp
                    bb[0] += bb[2]  # vx
                    bb[1] += bb[3]  # vy
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 15  # Giữ nguyên 15 cho boss lv3 nâng cấp
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[0] < -50 or bb[0] > WIDTH + 50 or bb[1] < -50 or bb[1] > HEIGHT + 50:
                        boss_bullets.remove(bb)

            # Boss bắn đạn
            if boss and current_time - last_boss_bullet_time > boss_bullet_delay and len(boss_bullets) < 300:
                if boss_level == 1 and not boss_entering:  # Chỉ bắn khi đã xuất hiện xong
                    # Tạo đạn mới cho boss lv1
                    boss_bullets.append(BossBulletLv1(
                        boss[0] + boss_img.get_width() // 2 - 20,
                        boss[1] + boss_img.get_height()
                    ))
                    last_boss_bullet_time = current_time
                elif boss_level == 2 and not boss_entering:  # Chỉ bắn khi đã xuất hiện xong
                    # Tăng thời gian giữa các lần bắn và tốc độ đạn
                    if len(boss_bullets) < 30:  # Giảm số lượng đạn tối đa
                        for angle in [-45, 0, 45]:
                            boss_bullets.append([
                                boss[0] + boss_img.get_width() // 2 - boss_bullet_img.get_width() // 2 + 10, 
                                boss[1] + boss_img.get_height(),
                                angle,
                                2
                            ])
                elif boss_level == 3 and not boss_entering:  # Chỉ bắn khi đã xuất hiện xong
                    if boss_lv3_upgraded:
                        # 🔹 Bắn plasma mỗi 5 giây
                        if current_time - last_plasma_time > PLASMA_INTERVAL:
                            gun_left = (boss[0] + 120, boss[1] + boss_img.get_height() - 105)
                            gun_right = (boss[0] + 280, boss[1] + boss_img.get_height() - 105)
                            plasma_beams.append(PlasmaBeam(*gun_left, is_left=True))
                            plasma_beams.append(PlasmaBeam(*gun_right, is_left=False))
                            last_plasma_time = current_time

                        # 🔸 Bắn đạn thường từ nòng trong
                        if current_time - last_inner_cannon_time > INNER_CANNON_INTERVAL:
                            last_inner_cannon_time = current_time
                            # Bắn từ nòng trong trái
                            boss_bullets.append([
                                boss[0] + 150,
                                boss[1] + 260,
                                0, 7,
                                3, 
                                "normal"
                            ])
                            # Bắn từ nòng trong phải
                            boss_bullets.append([
                                boss[0] + 250,
                                boss[1] + 260,
                                0, 7,
                                3,
                                "normal"
                            ])

                    else:
                        # Boss thường: bắn vòng tròn
                        num_bullets = 20
                        center_x = boss[0] + boss_img.get_width() // 2
                        center_y = boss[1] + boss_img.get_height() // 2
                        speed = 3
                        for i in range(num_bullets):
                            angle = (2 * math.pi / num_bullets) * i
                            vx = speed * math.cos(angle)
                            vy = speed * math.sin(angle)
                            boss_bullets.append([
                                center_x, center_y, vx, vy,
                                3  # Boss level
                            ])

                last_boss_bullet_time = current_time

            # Gà bắn đạn
            current_time = pygame.time.get_ticks()
            visible_chickens = []  # Khởi tạo danh sách rỗng để tránh lỗi UnboundLocalError

            if current_time - last_enemy_shot_time > enemy_fire_delay and chickens and len(enemy_bullets) < MAX_ENEMY_BULLETS:
                visible_chickens = [c for c in chickens if c[1] > 0]  # Chỉ chọn gà đã xuất hiện

                if visible_chickens:  # Kiểm tra danh sách có phần tử không
                    # Chỉ cho phép một số lượng gà nhất định bắn đạn
                    shooting_chickens = random.sample(visible_chickens, min(MAX_SHOOTING_CHICKENS, len(visible_chickens)))
                    for chicken in shooting_chickens:
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

            # Tạo hộp quà rơi
            current_time = pygame.time.get_ticks()
            if boss1_chet and current_time - last_gift_spawn_time > gift_spawn_delay:  # Chỉ spawn sau khi giết boss lv1
                new_gift = [random.randint(0, WIDTH - 40), -40]  # Thêm hộp quà mới
                gifts.append(new_gift)
                last_gift_spawn_time = current_time
                gift_spawn_delay = random.randint(15000, 25000)  # 15-25 giây spawn một hộp quà

            # Di chuyển và kiểm tra va chạm hộp quà
            for gift in gifts[:]:
                gift[1] += gift_speed
                # Cập nhật góc xoay
                gift_rotation = (gift_rotation + 2) % 360  # Xoay 2 độ mỗi frame
                # Xoay hộp quà
                rotated_gift = pygame.transform.rotate(gift_img, gift_rotation)
                # Lấy rect mới sau khi xoay để căn giữa
                gift_rect = rotated_gift.get_rect(center=(gift[0] + gift_img.get_width()//2, 
                                                        gift[1] + gift_img.get_height()//2))
                
                # Kiểm tra va chạm với tàu
                if ((gift_rect.centerx - ship_x) ** 2 + (gift_rect.centery - ship_y) ** 2) ** 0.5 < 40:
                    # Nâng cấp vũ khí
                    weapon_level = min(weapon_level + 1, 4)  # Tăng cấp độ vũ khí, tối đa là 4
                    gifts.remove(gift)
                # Xóa hộp quà nếu ra khỏi màn hình
                elif gift[1] > HEIGHT:
                    gifts.remove(gift)

            # Di chuyển đạn của tàu
            for b in bullets[:]:
                b[1] -= 4
                if b[1] < 0:
                    bullets.remove(b)

            # Di chuyển đạn của gà 
            for eb in enemy_bullets[:]:
                eb[1] += 2  # Điều chỉnh tốc độ bắn
                if eb[1] > HEIGHT:
                    enemy_bullets.remove(eb)

           # Di chuyển đạn của boss
            for bb in boss_bullets[:]:
                if isinstance(bb, BossBulletLv1):
                    bb.update()
                    # Kiểm tra va chạm với tàu
                    if ((bb.x - ship_center_x) ** 2 + (bb.y - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 10
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        bb.active = False
                    if not bb.active:
                        boss_bullets.remove(bb)
                elif len(bb) == 4 and bb[3] == 2:  # Boss lv2
                    # Di chuyển đạn theo góc
                    bb[1] += 4  # Tăng tốc độ di chuyển xuống
                    bb[0] += math.sin(math.radians(bb[2])) * 2  # Tăng tốc độ di chuyển ngang
                    
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 10
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[1] > HEIGHT + 50:
                        boss_bullets.remove(bb)
                elif len(bb) == 5 and bb[4] == 3:  # Boss lv3 thường
                    bb[0] += bb[2]  # vx
                    bb[1] += bb[3]  # vy
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 10
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[0] < -50 or bb[0] > WIDTH + 50 or bb[1] < -50 or bb[1] > HEIGHT + 50:
                        boss_bullets.remove(bb)
                elif len(bb) == 6 and bb[4] == 3:  # Boss lv3 nâng cấp
                    bb[0] += bb[2]  # vx
                    bb[1] += bb[3]  # vy
                    # Kiểm tra va chạm với tàu
                    if ((bb[0] - ship_center_x) ** 2 + (bb[1] - ship_center_y) ** 2) ** 0.5 < 40:
                        ship_health -= 10
                        damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                        boss_bullets.remove(bb)
                    # Kiểm tra nếu đạn ra khỏi màn hình
                    elif bb[0] < -50 or bb[0] > WIDTH + 50 or bb[1] < -50 or bb[1] > HEIGHT + 50:
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
                boss_center_x = boss[0] + boss_img.get_width() // 2
                boss_center_y = boss[1] + boss_img.get_height() // 2

                boss_rect = pygame.Rect(boss[0], boss[1], boss_img.get_width(), boss_img.get_height())

                for b in bullets[:]:
                    if isinstance(b, list) and len(b) >= 2:
                        bullet_rect = pygame.Rect(b[0] + 10, b[1] + 10, bullet.get_width() - 20, bullet.get_height() - 20)
                        if boss_rect.colliderect(bullet_rect):
                            bullets.remove(b)
                            # Giảm sát thương cho boss level 3
                            if boss_level == 3:
                                boss_health -= 5  # Giảm từ 10 xuống 5 cho boss level 3
                            else:
                                boss_health -= 10  # Giữ nguyên sát thương cho boss level 1 và 2
                            if boss_level == 3 and not boss_lv3_upgraded and boss_health <= menu.game_enemy_variables["boss_health"] * 0.2:
                                # Kích hoạt hiệu ứng nâng cấp và rung chấn cùng lúc
                                shake_time = 150
                                boss_message_display_time = 2500
                                current_boss_message = "upgrade"
                                boss_lv3_upgraded = True
                                boss_health = 800
                                boss_img = boss_lv3_frames[1]
                                pg.mixer.music.stop()
                                pg.mixer.music.load("data/nhacnen2.mp3")
                                pg.mixer.music.play(-1)
                            if boss_health <= 0:
                                print(f"🔥 Boss {boss_level} bị tiêu diệt, đặt boss = None")
                                # Xóa plasma beam ngay khi boss chết
                                if boss_level == 3 and boss_lv3_upgraded:
                                    plasma_beams.clear()
                                boss = None
                                boss_speed = 0
                                boss_health = 0

                                if boss_level == 1:
                                    boss1_chet = True
                                    boss_level = 2
                                elif boss_level == 2:
                                    boss2_chet = True
                                    boss_level = 3
                                elif boss_level == 3:
                                    print("🎉 Boss level 3 đã tiêu diệt - Kết thúc hoặc chuyển cảnh!")

                                boss_respawn_time = pygame.time.get_ticks()
                                break

            # Kiểm tra khi boss lv3 nâng cấp
            if (boss_level == 3 and boss is not None and 
                not boss_lv3_upgraded and 
                boss_health <= menu.game_enemy_variables["boss_health"] * 0.2):
                # Kích hoạt hiệu ứng nâng cấp và rung chấn cùng lúc
                shake_time = 150
                boss_message_display_time = 2500
                current_boss_message = "upgrade"
                boss_lv3_upgraded = True
                boss_health = 800
                boss_img = boss_lv3_frames[1]
                pg.mixer.music.stop()
                pg.mixer.music.load("data/nhacnen2.mp3")
                pg.mixer.music.play(-1)

            # Kiểm tra nếu đạt điểm để xuất hiện boss cấp 1
            if score >= 5 and boss is None and boss_level == 1 and not pending_boss_spawn:
                shake_time = 150
                boss_message_display_time = 2500
                pending_boss_spawn = True

            # Kiểm tra nếu đạt điểm để xuất hiện boss cấp 2
            if score >= 10 and boss is None and boss_level == 2 and not pending_boss_spawn:
                shake_time = 150
                boss_message_display_time = 2500
                pending_boss_spawn = True

            # Kiểm tra nếu đạt điểm để xuất hiện boss cấp 3
            if score >= 15 and boss is None and boss_level == 3 and not pending_boss_spawn:
                shake_time = 150
                boss_message_display_time = 2500
                pending_boss_spawn = True
                boss_lv3_upgraded = False  # Reset trạng thái nâng cấp

            # Khi rung chấn kết thúc, mới tạo boss
            if pending_boss_spawn and shake_time == 0 and boss is None:
                if boss_level == 1:
                    boss = [WIDTH // 2 - 50, -100]  # Bắt đầu từ trên màn hình
                    boss_speed = 0.8
                    boss_img = pygame.image.load("data/boss1.png")
                    boss_img = pygame.transform.scale(boss_img, (100, 100))
                    boss_health = 300
                    current_boss_message = "normal"
                    boss_entering = True
                elif boss_level == 2:
                    boss = [WIDTH // 2 - 60, -120]  # Bắt đầu từ trên màn hình
                    boss_speed = 0.8
                    boss_img = boss_img_lv2
                    boss_health = 400
                    current_boss_message = "normal"
                    boss_entering = True
                elif boss_level == 3:
                    boss = [WIDTH // 2 - 75, -150]  # Bắt đầu từ trên màn hình
                    boss_speed = 1.0
                    boss_health = 500
                    boss_img = boss_lv3_frames[0]
                    boss_bullet_delay = 2500
                    boss_entering = True  # Thêm biến để kiểm soát trạng thái xuất hiện
                    if not boss_lv3_upgraded:
                        current_boss_message = "normal"
                    else:
                        current_boss_message = None

                pending_boss_spawn = False

            # Cập nhật vị trí boss
            if boss is not None:
                if (boss_level == 1 or boss_level == 2 or boss_level == 3) and boss_entering:
                    # Di chuyển xuống cho đến khi đạt vị trí mong muốn
                    if boss[1] < 50:  # Vị trí cuối cùng
                        boss[1] += 2  # Tốc độ di chuyển xuống
                    else:
                        boss_entering = False  # Kết thúc hiệu ứng xuất hiện
                else:
                    # Di chuyển qua lại bình thường
                    boss[0] += boss_speed
                    if boss[0] <= 0 or boss[0] >= WIDTH - boss_img.get_width():
                        boss_speed = -boss_speed

            # Hiển thị chữ boss - Đảm bảo chỉ hiển thị một thông báo tại một thời điểm
            if boss_message_display_time > 0 and current_boss_message is not None:
                # Xóa màn hình trước khi vẽ thông báo mới
                screen.fill((0, 0, 0))
                screen.blit(background, (0, background_y))
                screen.blit(background, (0, background_y - HEIGHT))
                
                # Áp dụng rung chấn nếu có
                if shake_time > 0:
                    apply_screen_shake(screen)
                
                if current_boss_message == "upgrade":
                    draw_boss_message(screen, boss_level, True)
                elif current_boss_message == "normal":
                    draw_boss_message(screen, boss_level, False)
                
                boss_message_display_time -= delta_time
                if boss_message_display_time <= 0:
                    current_boss_message = None

            # Hiển thị vụ nổ
            for explosion in explosions[:]:
                screen.blit(explosion_img, (explosion[0], explosion[1]))
                if pygame.time.get_ticks() - explosion[2] > 500:  # Hiển thị trong 500ms
                    explosions.remove(explosion)        

            # Kiểm tra va chạm giữa đạn của gà và tàu
            for eb in enemy_bullets[:]:
                if ((eb[0] - ship_x) ** 2 + (eb[1] - ship_y) ** 2) ** 0.5 < 40:
                    ship_health -= 10
                    damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
                    enemy_bullets.remove(eb)

        
            # Hiển thị đạn của boss
            for bb in boss_bullets:
                if isinstance(bb, BossBulletLv1):
                    bb.draw(screen)
                elif len(bb) == 4 and bb[3] == 2:  # Boss lv2
                    # Vẽ hiệu ứng glow
                    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    # Vẽ glow bên ngoài
                    pygame.draw.circle(glow_surface, (255, 0, 0, 50), 
                                    (int(bb[0] + 20), int(bb[1] + 20)), 
                                    25)
                    # Vẽ glow bên trong
                    pygame.draw.circle(glow_surface, (255, 0, 0, 100), 
                                    (int(bb[0] + 20), int(bb[1] + 20)), 
                                    15)
                    screen.blit(glow_surface, (0, 0))
                    
                    # Vẽ đạn chính
                    screen.blit(boss_bullet, (bb[0], bb[1]))
                elif len(bb) == 5 and bb[4] == 3:  # boss level 3
                    angle = math.degrees(math.atan2(bb[3], bb[2])) - 90
                    rotated_bullet = pygame.transform.rotate(boss_bullet_img_lv3, -angle)
                    bullet_rect = rotated_bullet.get_rect(center=(bb[0], bb[1]))
                    screen.blit(rotated_bullet, bullet_rect.topleft)
                elif len(bb) == 6 and bb[4] == 3:  # boss level 3 nâng cấp
                    angle = math.degrees(math.atan2(bb[3], bb[2])) - 90
                    rotated_bullet = pygame.transform.rotate(boss_bullet_img_lv3, -angle)
                    bullet_rect = rotated_bullet.get_rect(center=(bb[0], bb[1]))
                    screen.blit(rotated_bullet, bullet_rect.topleft)
                else:
                    screen.blit(boss_bullet_img, (bb[0], bb[1]))



            
            if boss is not None:
                boss[0] += boss_speed
                if boss[0] <= 0 or boss[0] >= WIDTH - boss_img.get_width():
                    boss_speed = -boss_speed
                
                if boss_level == 1:
                    screen.blit(boss_img, (boss[0], boss[1]))
                elif boss_level == 2:
                    screen.blit(boss_img_lv2, (boss[0], boss[1]))
                elif boss_level == 3:
                    frame_index = 1 if boss_lv3_upgraded else 0
                    screen.blit(boss_lv3_frames[frame_index], (boss[0], boss[1]))



            # Kiểm tra Game Over
            if ship_health <= 0:
                game_over = True
                # Xóa plasma beam khi game over
                plasma_beams.clear()

        # Cập nhật plasma và kiểm tra va chạm
        for beam in plasma_beams[:]:
            if boss is not None:  # Chỉ cập nhật khi boss còn sống
                beam.update(boss[0])  # Truyền vị trí x của boss
                # Kiểm tra va chạm với tàu
                if beam.check_collision(ship_x, ship_y, ship.get_width(), ship.get_height()):
                    ship_health -= 15  # Tăng từ 10 lên 15 máu mỗi lần
                    damage_flash_time = 30  # Kích hoạt hiệu ứng chớp nháy
            if not beam.active:
                plasma_beams.remove(beam)

        # Vẽ plasma
        for beam in plasma_beams:
            beam.draw(screen)
        

        # Vẽ tàu, gà, đạn
        if not game_over:
            # Vẽ vệt sáng trước
            for i, (trail_x, trail_y) in enumerate(ship_trail):
                # Tính độ trong suốt dựa trên vị trí trong trail
                alpha = int(120 * (i + 1) / len(ship_trail))  # Nhạt hơn, max 120
                faded_ship = ship.copy()
                faded_ship.set_alpha(alpha)
                screen.blit(faded_ship, (trail_x, trail_y))

            # Vẽ tàu với hiệu ứng chớp nháy
            if damage_flash_time > 0:
                if damage_flash_time % 4 == 0:
                    screen.blit(ship, (ship_x, ship_y))
            else:
                screen.blit(ship, (ship_x, ship_y))

            # Vẽ gà
            for chicken_x, chicken_y in chickens:
                screen.blit(chicken_img, (chicken_x, chicken_y))

            # Vẽ đạn
            for b in bullets:
                screen.blit(bullet, (b[0], b[1]))
            for eb in enemy_bullets:
                screen.blit(enemy_bullet, (eb[0], eb[1]))

            # Vẽ hộp quà
            for gift in gifts:
                # Xoay hộp quà
                rotated_gift = pygame.transform.rotate(gift_img, gift_rotation)
                # Lấy rect mới sau khi xoay để căn giữa
                gift_rect = rotated_gift.get_rect(center=(gift[0] + gift_img.get_width()//2, 
                                                        gift[1] + gift_img.get_height()//2))
                screen.blit(rotated_gift, gift_rect.topleft)

            # Vẽ cục máu
            for h in hearts:
                screen.blit(heart_img, (h[0], h[1]))

            # Hiển thị điểm số với font RetroFont
            score_font = pygame.font.Font("fonts/RetroFont.ttf", 30)
            score_text = score_font.render(f"SCORE: {score}", True, (255, 255, 255))
            # Thêm bóng đổ cho text
            shadow = score_font.render(f"SCORE: {score}", True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(WIDTH - 90 + 2, 30 + 2))
            score_rect = score_text.get_rect(center=(WIDTH - 90, 30))
            screen.blit(shadow, shadow_rect)
            screen.blit(score_text, score_rect)

            # Hiển thị thanh máu
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, ship_health * 2, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20), 2)

            # Hiển thị cấp độ vũ khí
            weapon_text = score_font.render(f"WEAPON: {weapon_level}", True, (255, 255, 255))
            weapon_shadow = score_font.render(f"WEAPON: {weapon_level}", True, (0, 0, 0))
            weapon_shadow_rect = weapon_shadow.get_rect(center=(WIDTH - 100 + 2, 60 + 2))
            weapon_rect = weapon_text.get_rect(center=(WIDTH - 100, 60))
            screen.blit(weapon_shadow, weapon_shadow_rect)
            screen.blit(weapon_text, weapon_rect)
        else:
            # Hiển thị màn hình Game Over
            game_over_text = FONT.render("GAME OVER!", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
            restart_button = draw_restart_button()  # Vẽ nút chơi lại
        clock.tick(60) 
        pygame.display.update()
        
        # Cập nhật thời gian chớp nháy
        if damage_flash_time > 0:
            damage_flash_time -= 1

# Main menu function
def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        # Draw title
        screen.blit(BG, (0, 0))
        screen.blit(text, textRect)

        update_buttons(menus["main_menu"])
        draw_buttons(menus["main_menu"])

        start_button = menus["main_menu"][0]
        option_button = menus["main_menu"][1]
        quit_button = menus["main_menu"][2]

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
                    options(game_enemy_variables)  # Open options menu
if __name__ == '__main__':
    main_menu()