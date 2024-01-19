import database
import pygame
import sys
import subprocess
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leaderboard")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (173, 216, 230)

# Fonts
font = pygame.font.Font(None, 36)

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


class Menu:
    def __init__(self):
        pass

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
                    '''for button in self.buttons:
                        button.update(mouse_pos)'''
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
diff_button = Button(100, 200, 200, 50, "Difficulty", RED, BLACK, command=["python", "app.py"])
lead_button = Button(100, 300, 200, 50, "Leaderboard", RED, BLACK, command=[])


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

MENU_PROMPT = """-- NBA Teams App--

Please choose one of these options:

1) Add a new team to the NBA.
2) See all NBA teams.
3) Find a team by name.
4) See how many championships a team has.
5) See a team's current record.
6) See a team's best player.
7) Delete a NBA team.
8) Sort all teams by number of championships. 
9) Sort all teams by their record in 2022-2023.
10) Exit.

Your selection:"""


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "10":
        if user_input == "1":
            prompt_add_new_team(connection)
        elif user_input == "2":
            prompt_see_all_teams(connection)
        elif user_input == "3":
            prompt_find_team(connection)
        elif user_input == "4":
            prompt_find_rings(connection)
        elif user_input == "5":
            prompt_find_team_record(connection)
        elif user_input == "6":
            prompt_find_player(connection)
        elif user_input == "7":
            prompt_delete_team(connection)
        elif user_input == "8":
            prompt_sort_by_rings(connection)
        elif user_input == "9":
            prompt_sort_by_record(connection)
        else:
            print("Invalid input, please try again!")


def prompt_add_new_team(connection):
    city = input("Enter your team's home city: ")
    name = input("Enter your team name: ")
    record = int(input("Enter your team's number of wins(in an 82 game season): "))
    rings = int(input("Enter your team's number of championships: "))
    history = int(input("Enter what year your team was founded: "))
    player = input("Enter the name of your team's best player: ")

    database.add_team(connection, city, name, record, rings, history, player)


def prompt_see_all_teams(connection):
    teams = database.get_all_teams(connection)

    for team in teams:
        print(f"The {team[1]} {team[2]} had a record of {team[3]}-{82 - team[3]} in 2022-2023. "
              f"They have {team[4]} championship(s) since they were founded in {team[5]}. "
              f"Their best player is {team[6]}. ")


def prompt_find_team(connection):
    name = input("Enter team name to find: ")
    teams = database.get_teams_by_name(connection, name)

    for team in teams:
        print(f"The {team[1]} {team[2]} had a record of {team[3]}-{82 - team[3]} in 2022-2023. "
              f"They have {team[4]} championship(s) since they were founded in {team[5]}. "
              f"Their best player is {team[6]}. ")


def prompt_find_rings(connection):
    name = input("Enter team name to find: ")
    teams = database.get_teams_by_name(connection, name)

    for team in teams:
        print(f"The {name} have {team[4]} championships. ")


def prompt_find_team_record(connection):
    name = input("Enter team name to find: ")
    teams = database.get_teams_by_name(connection, name)

    for team in teams:
        print(f"The {name} had a record of {team[3]}-{82 - team[3]} in 2022-2023. ")


def prompt_find_player(connection):
    name = input("Enter team name to find: ")
    teams = database.get_teams_by_name(connection, name)

    for team in teams:
        print(f"The {name}' best player is {team[6]}. ")


def prompt_delete_team(connection):
    name = input("Enter name of bean you want to delete: ")
    delete = database.delete_team(connection, name)

    print(f"You deleted {name} ")


def prompt_sort_by_rings(connection):
    teams = database.sort_by_rings(connection)

    for team in teams:
        print(f"The {team[1]} {team[2]} have {team[4]} championships.")


def prompt_sort_by_record(connection):
    teams = database.sort_by_record(connection)

    for team in teams:
        print(f"The {team[1]} {team[2]} had a record of {team[3]}-{82 - team[3]} in 2022-2023. ")



menu()