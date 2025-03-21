import pygame, sys
from UI import Button

# Initialize pygame
pygame.init()

# Game window configuration
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load background image
BG_img = pygame.image.load("game/data/menu_bg.jpg")
BG = pygame.transform.scale(BG_img, (WIDTH, HEIGHT))

# Font setup
Font = pygame.font.Font(None, 50)
# Font chữ hiển thị

font = pygame.font.SysFont("impact", 170)  # font name and size
text = font.render("CHICKEN INVADERS", False, (100,255,100)) # surface for text
textRect = text.get_rect()
textRect.center = (WIDTH//2, HEIGHT//2 - 200)  # center of text is screen center

# Create buttons
buttons = [
    Button(screen, (WIDTH // 2, HEIGHT // 2), "START"),
    Button(screen, (WIDTH // 2, HEIGHT // 2 + 150), "OPTIONS"),
    Button(screen, (WIDTH // 2, HEIGHT // 2 + 300), "QUIT"),
]

# Function to draw buttons
def draw():
    for button in buttons:
        button.draw()

# Update buttons when an event occurs
def update():
    for button in buttons:
        button.update()

# Main menu function
def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        # Draw title
        screen.blit(BG, (0, 0))
        screen.blit(text, textRect)

        draw()
        update()

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
                    print("Game Starting...")  # Placeholder for starting the game
                    return  
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if option_button.rect.collidepoint(event.pos):
                    options()  # Open options menu

# Options menu function
def options():
    running = True
    while running:
        screen.blit(BG, (0, 0))

        # Render options text
        options_text = Font.render("OPTIONS MENU", True, (255, 255, 255))
        screen.blit(options_text, (WIDTH // 2 - 120, HEIGHT // 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Return to main menu

# Run main menu
main_menu()
