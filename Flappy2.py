import pygame, random, time, sys, os
from pygame.locals import *
import pygame
from pygame.locals import *
from pygame import mixer


mixer.init()
mixer.music.load('assets/audio/rain.mp3')
mixer.music.play()

pygame.init()
pygame.font.init()

# VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
score = 0
score_display = pygame.font.Font('freesansbold.ttf')
pass_pipe = False
GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT = 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500


PIPE_GAP = 150

wing = 'assets/audio/chime.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        # Update height with boundary check
        if self.rect[1] < 0:
            self.rect[1] = 0
            self.speed = 0  # Reset speed when hitting the top boundary

        self.rect[1] += self.speed

        # Additional condition to prevent going beyond a certain height
        max_height = SCREEN_HEIGHT - 100
        if self.rect[1] > max_height:
            self.rect[1] = max_height
            self.speed = 0  # Reset speed when reaching the maximum height
    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
            self.direction = 5
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
            self.direction = -1

        self.mask = pygame.mask.from_surface(self.image)

        self.amplitude = -5 #speed
        self.frequency = 3.0 #up and down
        self.time = 2

    def update(self):
        self.rect[0] -= GAME_SPEED

        # Update the y-coordinate based on the direction of motion
        self.rect[1] += self.direction * self.amplitude * pygame.math.Vector2(0, 1).rotate(self.frequency * self.time).y
        self.time += 1

        # Change the direction when the pipe reaches the top or bottom of the screen
        if self.direction == -1 and self.rect.top < 0:
            self.direction = 1  # Change to downward motion
        elif self.direction == 1 and self.rect.bottom > SCREEN_HEIGHT:
            self.direction = -1  # speed


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/spaceee.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(0, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)

    # Define the scoring rectangle
    score_rectangle = pygame.Rect(xpos + PIPE_WIDHT // 2 - 5, 0, 10, SCREEN_HEIGHT)

    return pipe, pipe_inverted, score_rectangle



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

DEFAULT_IMAGE_SIZE = (250, 250)
BACKGROUND = pygame.image.load('assets/sprites/background11.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/img_19.png').convert_alpha()
BEGIN_IMAGE = pygame.transform.scale(BEGIN_IMAGE, DEFAULT_IMAGE_SIZE)

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

for i in range(2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

begin = True

while begin:
    spin_duration = 2  # in seconds
    start_time = time.time()
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False



    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

while True:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDHT * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False,   pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        break
score_display(score)
screen = pygame.display.set_mode((750, 450))
clock = pygame.time.Clock()
player = pygame.Rect(100, 200, 50, 50)
obstacle = pygame.Rect(200, 200, 50, 50)
while True:
    font = pygame.font.Font(None, 36)