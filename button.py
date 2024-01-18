import pygame
import sys
import subprocess

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (173, 216, 230)

# Fonts
font = pygame.font.Font(None, 36)

# Create buttons
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, command=None, submenu=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.command = command
        self.submenu = submenu

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

# Create a Menu class to handle different groups of buttons
class Menu:
    def __init__(self, buttons):
        self.buttons = buttons

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.command:
                                if button.command[0] == "quit":
                                    running = False
                                    pygame.quit()
                                    sys.exit()
                                else:
                                    subprocess.run(button.command)
                            elif button.submenu:
                                button.submenu.run()

            # Draw the buttons
            screen.fill(BLUE)
            for button in self.buttons:
                button.draw(screen)

            pygame.display.flip()

# Create buttons for different game options
flappy_button = Button(100, 200, 200, 50, "Flappy Mode", RED, BLACK, command=["python", "flappy.py"])
flappy2_button = Button(100, 300, 200, 50, "Flappy2 Mode", RED, BLACK, command=["python", "flappy2.py"])
quit_button = Button(100, 400, 200, 50, "Quit", RED, BLACK, command=["quit"])

# Create a submenu for different game options
game_submenu = Menu([flappy_button, flappy2_button, quit_button])

# Create a top-level menu with the submenu option
main_menu = Menu([Button(100, 100, 200, 50, "Select Game", RED, BLACK, submenu=game_submenu)])

# Run the main menu
main_menu.run()
