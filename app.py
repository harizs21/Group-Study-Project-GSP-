import database
import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leaderboard")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def display_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

MENU_PROMPT = """-- NBA yu--

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

    while True:
        screen.fill((0, 0, 0))

        display_text(MENU_PROMPT, 20, 20)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    prompt_add_new_team(connection)
                elif event.key == pygame.K_2:
                    prompt_see_all_teams(connection)
                elif event.key == pygame.K_3:
                    prompt_find_team(connection)
                elif event.key == pygame.K_4:
                    prompt_find_rings(connection)
                elif event.key == pygame.K_5:
                    prompt_find_team_record(connection)
                elif event.key == pygame.K_6:
                    prompt_find_player(connection)
                elif event.key == pygame.K_7:
                    prompt_delete_team(connection)
                elif event.key == pygame.K_8:
                    prompt_sort_by_rings(connection)
                elif event.key == pygame.K_9:
                    prompt_sort_by_record(connection)
                elif event.key == pygame.K_0:
                    pygame.quit()
                    quit()
                else:
                    print("Invalid input, please try again!")

        clock.tick(30)  # Adjust the frame rate as needed


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