import pygame, sys
from UI import Button


# Initialize pygame
pygame.init()
input_map = {
            'Move Right': pygame.K_RIGHT,
            'Move Left': pygame.K_LEFT,
            'Move Up': pygame.K_UP,
            'Move Down': pygame.K_DOWN,
            'Shoot': pygame.K_SPACE
}

game_enemy_variables = {
            'current_mode': "easy",
            'chicken_speed': 0.5,
            'heart_speed': 2,
            'enemy_fire_delay': 3000,
            'boss_bullet_delay': 1000,
            'boss_health': 1000,
}

game_ship_variables = {
            'ship_speed': 4,
            'ship_health': 100,
            'fire_delay': 250, # Tốc độ bắn của tàu
}


# Game window configuration
WIDTH, HEIGHT = 1024, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load background image
BG_img = pygame.image.load("data/menu_bg.png")
BG = pygame.transform.scale(BG_img, (WIDTH, HEIGHT))

# Font setup
Fontt = pygame.font.Font("fonts\RetroFont.ttf", 40)
FontTitle = pygame.font.Font("fonts\RetroFont.ttf", 70)

# Font chữ hiển thị
# font name and size
font = pygame.font.Font("fonts\RetroFont.ttf", 80)  
# surface cho text
text = font.render("CHICKEN INVADERS", False, (100,255,100)) 
textRect = text.get_rect()
# vị trí center của title của game
textRect.center = (WIDTH//2, HEIGHT//2 - 200)  

# load ảnh cho các button
# Start
start_button_img = pygame.image.load("data/buttons/Start_Button.png")
start_button = pygame.transform.scale(start_button_img, (298.5, 135.5))

# Options
option_button_img = pygame.image.load("data/buttons/Option_Button.png")
option_button = pygame.transform.scale(option_button_img, (298.5, 135.5))

# Quit
quit_button_img = pygame.image.load("data/buttons/Quit_Button.png")
quit_button = pygame.transform.scale(quit_button_img, (298.5, 135.5))

# Keybind (ở options menu)
keybind_button_img = pygame.image.load("data/buttons/Keybind_Button.png")
keybind_button = pygame.transform.scale(keybind_button_img, (298.5, 135.5))

# Return (ở pause menu, options menu)
return_button_img = pygame.image.load("data/buttons/Return_Button.png")
return_button = pygame.transform.scale(return_button_img, (298.5, 135.5))

# To Menu (ở pause menu)
to_menu_button_img = pygame.image.load("data/buttons/To_Menu_Button.png")
to_menu_button = pygame.transform.scale(to_menu_button_img, (298.5, 135.5))

#Easy Medium Hard
Easy_Button_img = pygame.image.load("data/buttons/Easy_Button.png")
Easy_Button = pygame.transform.scale(Easy_Button_img, (298.5, 135.5))

Medium_Button_img = pygame.image.load("data/buttons/Medium_Button.png")
Medium_Button = pygame.transform.scale(Medium_Button_img, (298.5, 135.5))

Hard_Button_img = pygame.image.load("data/buttons/Hard_Button.png")
Hard_Button = pygame.transform.scale(Hard_Button_img, (298.5, 135.5))

# Gán các ảnh này vào từng button tương ứng
menus = {
    "main_menu": [
        Button((WIDTH // 2, HEIGHT // 2), "START", "",image=start_button),
        Button((WIDTH // 2, HEIGHT // 2 + 150), "OPTIONS", "",image=option_button),
        Button((WIDTH // 2, HEIGHT // 2 + 300), "QUIT", "",image=quit_button),
    ],
    "options_menu": [
        Button((WIDTH // 2, HEIGHT // 2 + 300), "Keybind", "",image=keybind_button),
        Button((WIDTH // 2, HEIGHT // 2 + 150), "RETURN", "",image=return_button),
    ],
    "pause_menu": [
        Button((WIDTH // 2, HEIGHT // 2 + 150), "RETURN", "",image=return_button),
        Button((WIDTH // 2, HEIGHT // 2), "TO MENU", "",image=to_menu_button),
        Button((WIDTH // 2, HEIGHT // 2 + 300), "QUIT", "",image=quit_button),
    ],
    "game_mode":[
        Button((WIDTH // 2 - 150, HEIGHT // 2), "EASY", "small", image=Easy_Button),
        Button((WIDTH // 2, HEIGHT // 2), "MEDIUM", "small", image=Medium_Button),
        Button((WIDTH // 2 + 150, HEIGHT // 2), "HARD",  "small",image=Hard_Button),
    ]
}

def draw_buttons(button_list):
    for button in button_list:
        button.draw(screen)

def update_buttons(button_list):
    for button in button_list:
        button.update()
        
FONT = pygame.font.Font(None, 40)

BG_COLOR = pygame.Color('gray12')
GREEN = pygame.Color('yellow')

        
def create_key_list(input_map = input_map):
    """Tạo 1 list gồm chứa bề mặt của các nút hành động + nút đã được chọn cho hành động đó và vị trí."""
    key_list = []
    for y, (action, value) in enumerate(input_map.items()):
        surf = Fontt.render('{}: {}'.format(action, pygame.key.name(value)), True, GREEN)
        rect = surf.get_rect(center=(WIDTH // 2, y * 40 + HEIGHT // 10))
        key_list.append([surf, rect, action])
    return key_list


def assignment_menu(input_map=input_map):
    selected_action = None

    while True:
        screen.blit(BG, (0, 0))
        key_list = create_key_list(input_map)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and selected_action is not None:
                input_map[selected_action] = event.key
                selected_action = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for UI buttons
                # RETURN
                if menus["pause_menu"][0].rect.collidepoint(event.pos):  
                    return input_map
                # TO MENU
                elif menus["pause_menu"][1].rect.collidepoint(event.pos):  
                    return main_menu()
                # QUIT
                elif menus["pause_menu"][2].rect.collidepoint(event.pos):  
                    pygame.quit()
                    sys.exit()

                # Kiểm tra nút binding nào được chọn
                for surf, rect, action in key_list:
                    if rect.collidepoint(event.pos):
                        selected_action = action

        # Vẽ các nút để thực hiện binding
        for surf, rect, action in key_list:
            screen.blit(surf, rect,)
            if selected_action == action:
                pygame.draw.rect(screen, GREEN, rect, 2)

        update_buttons(menus["pause_menu"])
        draw_buttons(menus["pause_menu"])

        pygame.display.flip()
        
def game_mode(events, game_enemy_variables = game_enemy_variables):
    for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # EASY
                if menus["game_mode"][0].rect.collidepoint(event.pos):
                    game_enemy_variables["current_mode"] = "EASY"
                    game_enemy_variables["chicken_speed"] = 0.5
                    game_enemy_variables["enemy_fire_delay"] = 3000
                    game_enemy_variables["boss_bullet_delay"] = 1000
                    game_enemy_variables["heart_speed"] = 2
                    game_enemy_variables["boss_health"] = 1000
                # MEDIUM
                elif menus["game_mode"][1].rect.collidepoint(event.pos):
                    game_enemy_variables["current_mode"] = "MEDIUM"
                    game_enemy_variables["chicken_speed"] = 0.5*1.5
                    game_enemy_variables["enemy_fire_delay"] = 3000*1.5
                    game_enemy_variables["boss_bullet_delay"] = 1000*1.5
                    game_enemy_variables["heart_speed"] = 2*1.5
                    game_enemy_variables["boss_health"] = 1000*1.5
                    
                # HARD
                elif menus["game_mode"][2].rect.collidepoint(event.pos):
                    game_enemy_variables["current_mode"] = "HARD"
                    game_enemy_variables["chicken_speed"] = 0.5*2
                    game_enemy_variables["enemy_fire_delay"] = 3000*2
                    game_enemy_variables["boss_bullet_delay"] = 1000*2
                    game_enemy_variables["heart_speed"] = 2*2
                    game_enemy_variables["boss_health"] = 1000*2
                print(game_enemy_variables)
    return game_enemy_variables
        
# Options menu
def options( game_enemy_variables):
    running = True
    volume = 0.3  # Giá trị mặc định 30%
    
    # Tạo thanh trượt âm lượng
    slider_width = 300
    slider_rect = pygame.Rect(WIDTH//2 - slider_width//2, HEIGHT//3 -50, slider_width, 20)
    knob_radius = 15
    knob_x = slider_rect.x + (slider_rect.width * volume)
    knob_rect = pygame.Rect(knob_x - knob_radius, slider_rect.centery - knob_radius,
                            knob_radius*2, knob_radius*2)
    
    # Biến để kiểm tra khi đang kéo thanh trượt
    dragging = False
    
    while running:
        screen.blit(BG, (0, 0))
        
        #tạo nút chỉnh độ khó
        mode_text = Fontt.render("Current Mode: " + game_enemy_variables["current_mode"], True, (0, 255, 0))
        if game_enemy_variables["current_mode"] == "EASY":
            mode_text = Fontt.render("Current Mode: " + game_enemy_variables["current_mode"], True, (0, 255, 0))
        if game_enemy_variables["current_mode"] == "MEDIUM":
            mode_text = Fontt.render("Current Mode: " + game_enemy_variables["current_mode"], True, (255, 255, 0))
        if game_enemy_variables["current_mode"] == "HARD":
            mode_text = Fontt.render("Current Mode: " + game_enemy_variables["current_mode"], True, (255, 0, 0))
        text_rect = mode_text.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 70))
        screen.blit(mode_text, text_rect.topleft)
        update_buttons(menus["game_mode"])
        draw_buttons(menus["game_mode"])
        
        # Vẽ label cho option
        options_text = FontTitle.render("OPTIONS MENU", True, (255, 255, 255))
        text_rect = options_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 300 ))
        screen.blit(options_text, text_rect.topleft)
        
        # Vẽ thanh trượt nền
        pygame.draw.rect(screen, (100, 100, 100), slider_rect, border_radius=10)
        # Vẽ phần âm lượng đã chọn
        filled_rect = pygame.Rect(slider_rect.x, slider_rect.y, 
                                slider_rect.width * volume, slider_rect.height)
        pygame.draw.rect(screen, (100, 255, 100), filled_rect, border_radius=10)
        # Vẽ nút trượt
        pygame.draw.circle(screen, (200, 200, 200), (knob_rect.centerx, knob_rect.centery), knob_radius)
        pygame.draw.circle(screen, (50, 50, 50), (knob_rect.centerx, knob_rect.centery), knob_radius-5)
        
        # Hiển thị giá trị âm lượng
        volume_text = Fontt.render(f"Volume: {int(volume * 100)}%", True, (255, 255, 255))

        # Căn giữa volume text dựa vào slider
        vol_text_rect = volume_text.get_rect(center=(slider_rect.centerx, slider_rect.top - 30))  # 30 pixel phía trên thanh trượt

        screen.blit(volume_text, vol_text_rect)
                
        # Cập nhật và vẽ các nút khác
        update_buttons(menus["options_menu"])
        draw_buttons(menus["options_menu"])

        events = pygame.event.get()
        game_enemy_variables = game_mode(events,game_enemy_variables)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menus["options_menu"][0].rect.collidepoint(event.pos):  
                # Keybind button
                    assignment_menu(input_map)
                if menus["options_menu"][1].rect.collidepoint(event.pos):  
                # Return button
                    return input_map
                # Kiểm tra click trên nút trượt
                elif knob_rect.collidepoint(event.pos):
                    dragging = True
                # Kiểm tra click trực tiếp trên thanh trượt
                elif slider_rect.collidepoint(event.pos):
                    volume = (event.pos[0] - slider_rect.x) / slider_rect.width
                    volume = max(0.0, min(1.0, volume))
                    knob_rect.centerx = slider_rect.x + (slider_rect.width * volume)
                    pygame.mixer.music.set_volume(volume)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Tính toán vị trí mới dựa trên vị trí chuột
                volume = (event.pos[0] - slider_rect.x) / slider_rect.width
                volume = max(0.0, min(1.0, volume))
                knob_rect.centerx = slider_rect.x + (slider_rect.width * volume)
                pygame.mixer.music.set_volume(volume)
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
from banGa import main_menu