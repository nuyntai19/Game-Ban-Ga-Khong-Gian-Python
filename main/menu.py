import pygame, sys
from UI import Button,Button1

input_map = {'move right': pygame.K_d, 'move left': pygame.K_a, 'move up': pygame.K_w, 'move down': pygame.K_s, 'shoot': pygame.K_SPACE}
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
    Button(screen, (WIDTH // 2, HEIGHT // 2), "START"),
    Button(screen, (WIDTH // 2, HEIGHT // 2 + 150), "OPTIONS"),
    Button(screen, (WIDTH // 2, HEIGHT // 2 + 300), "QUIT"),
]
buttons1 = [
    Button1(screen, (WIDTH // 2, HEIGHT // 2 + 300), "Keybind")
]



# Function to draw buttons
def draw():
    for button in buttons:
        button.draw()

# Update buttons when an event occurs
def update():
    for button in buttons:
        button.update()
def draw1():
    for button1 in buttons1:
        button1.draw1()

# Update buttons when an event occurs
def update1():
    for button1 in buttons1:
        button1.update1()
        
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


def assignment_menu(input_map = input_map):
    """Allow the user to change the key assignments in this menu.

    The user can click on an action-key pair to select it and has to press
    a keyboard key to assign it to the action in the `input_map` dict.
    """
    selected_action = None
    key_list = create_key_list(input_map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if selected_action is not None:
                    # Assign the pygame key to the action in the input_map dict.
                    input_map[selected_action] = event.key
                    selected_action = None
                    # Need to re-render the surfaces.
                    key_list = create_key_list(input_map)
                if event.key == pygame.K_ESCAPE:  # Leave the menu.
                    # Return the updated input_map dict to the main function.
                    return input_map
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_action = None
                for surf, rect, action in key_list:
                    # See if the user clicked on one of the rects.
                    if rect.collidepoint(event.pos):
                        selected_action = action

        screen.fill(BG_COLOR)
        # Blit the action-key table. Draw a rect around the
        # selected action.
        for surf, rect, action in key_list:
            screen.blit(surf, rect)
            if selected_action == action:
                pygame.draw.rect(screen, GREEN, rect, 2)

        pygame.display.flip()        
        
# Options menu function
def options():
    running = True
    while running:
        screen.blit(BG, (0, 0))

        # Render options text
        options_text = Font.render("OPTIONS MENU", True, (255, 255, 255))
        screen.blit(options_text, (WIDTH // 2 - 120, HEIGHT // 4))
        
        draw1()
        update1()

        keybind_button = buttons1[0]

        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if keybind_button.rect.collidepoint(event.pos):
                    assignment_menu(input_map)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Return to main menu
