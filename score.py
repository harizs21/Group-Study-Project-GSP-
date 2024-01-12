import pygame
class Score:
    def __init__(self):
        self.score = 0
        self.font = None
        self.x = 10
        self.y = 10

    def set_font(self, font):
        self.font = font

    def increase_score(self, points=1):
        self.score += points

    def reset_score(self):
        self.score = 0

    def draw(self, screen):
        if self.font:
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (self.x, self.y))