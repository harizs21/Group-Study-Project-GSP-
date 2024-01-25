import pygame
import sys
import subprocess
import database

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
def run_command(command):
    if callable(command):  # Check if command is a function
        command()
    elif command[0] == "quit":
        pygame.quit()
        sys.exit()
    else:
        subprocess.run(command)
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
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.command:
                                run_command(button.command)
                            elif button.submenu:
                                button.submenu.run()

            # Draw the buttons
            screen.fill(BLUE)
            for button in self.buttons:
                button.draw(screen)

            pygame.display.flip()

def display_leaderboard():
    connection = database.connect()
    display_sorted_scores(connection)  # Assuming you have a function to display scores

def display_sorted_scores(connection):
    screen.fill((0, 0, 0))  # Fill the screen with a black background

    database.create_tables(connection)
    sorted_scores = database.sort_by_scores(connection)

    # Display the sorted scores on the screen
    font = pygame.font.Font(None, 36)
    y_position = 20  # Starting y-position for the first score

    for i, score_data in enumerate(sorted_scores):
        score_text = font.render(f"{i + 1}. {score_data[1]}: {score_data[2]}", True, (255, 255, 255))
        screen.blit(score_text, (20, y_position))
        y_position += 40  # Adjust this value to control the vertical spacing between scores

    pygame.display.flip()  # Update the display



# Buttons
flappy_button = Button(100, 200, 200, 50, "Flappy Mode", RED, BLACK, command=["python", "flappy.py"])
flappy2_button = Button(100, 300, 200, 50, "Flappy2 Mode", RED, BLACK, command=["python", "flappy2.py"])
quit_button = Button(100, 400, 200, 50, "Quit", RED, BLACK, command=sys.exit)
diff_button = Button(100, 300, 200, 50, "Difficulty", RED, BLACK, command=["python", "app.py"])

# Submenu for start
start_game_submenu = Menu([flappy_button, flappy2_button])
start_button = Button(100, 200, 200, 50, "Start", RED, BLACK, submenu=start_game_submenu)

# Menu with the submenu option
main_menu = Menu([start_button, diff_button, quit_button])

# Run the main menu
main_menu.run()
