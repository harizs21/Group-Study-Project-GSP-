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

'''# Create buttons
start_button = Button(100, 200, 200, 50, "Start", RED, BLACK)
choose_button = Button(100, 300, 200, 50, "Chose", RED, BLACK)
quit_button = Button(100, 400, 200, 50, "Quit", RED, BLACK)'''
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

# Buttons
flappy_button = Button(100, 200, 200, 50, "Flappy Mode", RED, BLACK, command=["python", "flappy.py"])
flappy2_button = Button(100, 300, 200, 50, "Flappy2 Mode", RED, BLACK, command=["python", "flappy2.py"])
quit_button = Button(100, 400, 200, 50, "Quit", RED, BLACK, command=["quit"])
diff_button = Button(100, 200, 200, 50, "Difficulty", RED, BLACK, command=[])
lead_button = Button(100, 300, 200, 50, "Leaderboard", RED, BLACK, command=["python", "app.py"])


easy_button = Button(100, 200, 200, 50, "Easy", RED, BLACK, command=[])
medium_button = Button(100, 300, 200, 50, "Medium", RED, BLACK, command=[])
hard_button = Button(100, 400, 200, 50, "Hard", RED, BLACK, command=["python", "flappy.py"])



# Submenu for difficulty options
difficulty_submenu = Menu([easy_button, medium_button, hard_button])
diff_button.submenu = difficulty_submenu


survive_the_snake = Button(100, 200, 200, 50, "Snake survival", RED, BLACK, command=["python", "flappyez.py"])
escape_broken_pipe = Button(100, 300, 200, 50, "broken Pipes", RED, BLACK, command=["python", "flappy2.py"])
classic_flappy = Button(100, 400, 200, 50, "Classic", RED, BLACK, command=["python", ""])

easy_options_submenu = Menu([survive_the_snake, escape_broken_pipe, classic_flappy])


survive_the_snake = Button(100, 200, 200, 50, "Ssssss", RED, BLACK, command=["python", "flappyez.py"])
escape_broken_pipe = Button(100, 300, 200, 50, "yur", RED, BLACK, command=["python", "flappy2.py"])
classic_flappy = Button(100, 400, 200, 50, "Classic", RED, BLACK, command=["python", ""])
# Submenu for easy options

medium_options_submenu = Menu([survive_the_snake, escape_broken_pipe, classic_flappy])

# Update the easy difficulty button with the submenu
easy_button.submenu = easy_options_submenu
medium_button.submenu = medium_options_submenu

# Submenu for options
options_game_submenu = Menu([diff_button, lead_button])
option_button = Button(100, 300, 200, 50, "Options", RED, BLACK, submenu=options_game_submenu)

# Submenu for start
start_game_submenu = Menu([flappy_button, flappy2_button])
start_button = Button(100, 200, 200, 50, "Start", RED, BLACK, submenu=start_game_submenu)

# Menu with the submenu option
main_menu = Menu([start_button, option_button, quit_button])

# Run the main menu
main_menu.run()
