# tiles.py
import pygame
from settings import TILESIZE, BLOCK_BROWN, GROUND_GRAY

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, kind="block"):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        if kind == "ground":
            self.draw_ground()

        elif kind == "block":
            self.draw_block()

        elif kind == "brick":
            self.draw_brick()

        elif kind == "question":
            self.draw_question()

        elif kind == "stone":
            self.draw_stone()

        elif kind == "pipe":
            self.draw_pipe()

        else:
            self.image.fill((255, 0, 255))  

        self.rect = self.image.get_rect(topleft=pos)

    def draw_ground(self):
        # base
        self.image.fill((110, 110, 110))

        # top highlight
        pygame.draw.rect(self.image, (150, 150, 150), (0, 0, TILESIZE, 8))

        # bottom shadow
        pygame.draw.rect(self.image, (75, 75, 75), (0, TILESIZE - 6, TILESIZE, 6))

    def draw_block(self):
        # floating platform block
        self.image.fill((145, 120, 85))

        # top highlight
        pygame.draw.rect(self.image, (175, 150, 110), (0, 0, TILESIZE, 6))

        # bottom shadow
        pygame.draw.rect(self.image, (95, 70, 45), (0, TILESIZE - 5, TILESIZE, 5))

    def draw_brick(self):
        self.image.fill((150, 75, 50))

        line_color = (100, 45, 30)

        # horizontal mortar line
        pygame.draw.line(
            self.image, line_color,
            (0, TILESIZE // 2), (TILESIZE, TILESIZE // 2), 2
        )

        # vertical mortar lines
        pygame.draw.line(
            self.image, line_color,
            (TILESIZE // 2, 0), (TILESIZE // 2, TILESIZE // 2), 2
        )
        pygame.draw.line(
            self.image, line_color,
            (TILESIZE // 4, TILESIZE // 2), (TILESIZE // 4, TILESIZE), 2
        )
        pygame.draw.line(
            self.image, line_color,
            (3 * TILESIZE // 4, TILESIZE // 2), (3 * TILESIZE // 4, TILESIZE), 2
        )

    def draw_question(self):
        self.image.fill((240, 180, 40))

        # border
        pygame.draw.rect(self.image, (180, 120, 20), (0, 0, TILESIZE, TILESIZE), 3)

        font = pygame.font.SysFont(None, 28)
        text = font.render("?", True, (90, 60, 0))
        text_rect = text.get_rect(center=(TILESIZE // 2, TILESIZE // 2))
        self.image.blit(text, text_rect)

    def draw_stone(self):
        self.image.fill((90, 90, 100))

        # inner border
        pygame.draw.rect(self.image, (130, 130, 140), (2, 2, TILESIZE - 4, TILESIZE - 4), 2)

        # cracks / detail
        pygame.draw.line(self.image, (70, 70, 80), (8, 10), (20, 18), 2)
        pygame.draw.line(self.image, (70, 70, 80), (22, 20), (30, 30), 2)

    def draw_pipe(self):
        #pipe body
        self.image.fill((30, 170, 40))

        #darker side shading
        pygame.draw.rect(self.image, (20, 120, 30), (0, 0, 6, TILESIZE))
        pygame.draw.rect(self.image, (20, 120, 30), (TILESIZE - 6, 0, 6, TILESIZE))

        #bright higlight strip
        pygame.draw.rect(self.image, (80, 220, 100), (8, 0, 6, TILESIZE))

        #top lip
        pygame.draw.rect(self.image, (25, 140, 35), (0, 0, TILESIZE, 8))
        