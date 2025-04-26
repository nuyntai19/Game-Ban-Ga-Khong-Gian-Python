import pygame, sys
from UI import Button


input_map = {'move right': pygame.K_RIGHT, 'move left': pygame.K_LEFT, 'move up': pygame.K_UP, 'move down': pygame.K_DOWN, 'shoot': pygame.K_SPACE}
# Initialize pygame
pygame.init()

# Game window configuration
WIDTH, HEIGHT = 1024, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load background image
BG_img = pygame.image.load("data/menu_bg.jpg")
BG = pygame.transform.scale(BG_img, (WIDTH, HEIGHT))

# Font setup
Font = pygame.font.Font(None, 40)
# Font chữ hiển thị

font = pygame.font.Font("fonts\RetroFont.ttf", 80)  # font name and size
text = font.render("CHICKEN INVADERS", False, (100,255,100)) # surface for text
textRect = text.get_rect()
textRect.center = (WIDTH//2, HEIGHT//2 - 200)  # center of text is screen center

# Create buttons
buttons = [
    Button((WIDTH // 2, HEIGHT // 2), "START"),
    Button((WIDTH // 2, HEIGHT // 2 + 150), "OPTIONS"),
    Button((WIDTH // 2, HEIGHT // 2 + 300), "QUIT"),
]
buttons1 = [
    Button((WIDTH // 2, HEIGHT // 2 + 300), "Keybind"),
]
buttons2 = [
    Button((WIDTH // 2, HEIGHT // 2 + 150), "RETURN"),
    Button((WIDTH // 2, HEIGHT // 2), "TO MENU"),
    Button((WIDTH // 2, HEIGHT // 2 + 300), "QUIT"),
]




def draw_buttons(button_list):
    for button in button_list:
        button.draw(screen)

def update_buttons(button_list):
    for button in button_list:
        button.update()


        
FONT = pygame.font.Font(None, 40)

BG_COLOR = pygame.Color('gray12')
GREEN = pygame.Color('lightseagreen')

        
def create_key_list(input_map = input_map):
    """A list of surfaces of the action names + assigned keys, rects and the actions."""
    key_list = []
    for y, (action, value) in enumerate(input_map.items()):
        surf = FONT.render('{}: {}'.format(action, pygame.key.name(value)), True, GREEN)
        rect = surf.get_rect(topleft=(40, y*40+20))
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
                if buttons2[0].rect.collidepoint(event.pos):  # RETURN
                    return input_map
                elif buttons2[1].rect.collidepoint(event.pos):  # TO MENU
                    return main_menu()
                elif buttons2[2].rect.collidepoint(event.pos):  # QUIT
                    pygame.quit()
                    sys.exit()

                # Check for keybinding clicks
                for surf, rect, action in key_list:
                    if rect.collidepoint(event.pos):
                        selected_action = action

        # Draw the keybinding text
        for surf, rect, action in key_list:
            screen.blit(surf, rect,)
            if selected_action == action:
                pygame.draw.rect(screen, GREEN, rect, 2)

        update_buttons(buttons2)
        draw_buttons(buttons2)

        pygame.display.flip()

        
# Options menu function
def options():
    running = True
    volume = 0.5  # Giá trị mặc định 50%
    
    # Tạo thanh trượt âm lượng
    slider_width = 300
    slider_rect = pygame.Rect(WIDTH//2 - slider_width//2, HEIGHT//2 + 50, slider_width, 20)
    knob_radius = 15
    knob_x = slider_rect.x + (slider_rect.width * volume)
    knob_rect = pygame.Rect(knob_x - knob_radius, slider_rect.centery - knob_radius, 
                           knob_radius*2, knob_radius*2)
    
    # Biến để kiểm tra khi đang kéo thanh trượt
    dragging = False
    
    while running:
        screen.blit(BG, (0, 0))

        # Render options text
        options_text = Font.render("OPTIONS MENU", True, (255, 255, 255))
        screen.blit(options_text, (WIDTH // 2 - 120, HEIGHT // 4))
        
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
        volume_text = Font.render(f"Volume: {int(volume*100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (WIDTH // 2 - 70, HEIGHT // 2 - 30))
        
        # Cập nhật và vẽ các nút khác
        update_buttons(buttons1)
        draw_buttons(buttons1)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons1[0].rect.collidepoint(event.pos):  # Keybind button
                    assignment_menu(input_map)
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
                knob_rect.centerx = slider_rect.x + (slobider_rect.width * volume)
                pygame.mixer.music.set_volume(volume)
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
from banGa import main_menu