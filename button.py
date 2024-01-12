import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Create buttons
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

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

# Create buttons
start_button = Button(300, 200, 200, 50, "Start", BLACK, WHITE)
choose_button = Button(300, 300, 200, 50, "Choose", BLACK, WHITE)
quit_button = Button(300, 400, 200, 50, "Quit", BLACK, WHITE)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            start_button.update(mouse_pos)
            choose_button.update(mouse_pos)
            quit_button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                # Add start button functionality here
                pass
            if choose_button.rect.collidepoint(event.pos):
                # Add choose button functionality here
                pass
            if quit_button.rect.collidepoint(event.pos):
                running = False
                pygame.quit()
                sys.exit()

    # Draw the buttons
    screen.fill(WHITE)
    start_button.draw(screen)
    choose_button.draw(screen)
    quit_button.draw(screen)

    # Add background image here

    pygame.display.flip()