# tiles.py
import pygame
from settings import TILESIZE, BLOCK_BROWN, GROUND_GRAY

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, kind="block"):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        if kind == "ground":
            self.image.fill(GROUND_GRAY)
        else:
            self.image.fill(BLOCK_BROWN)   # floating blocks
        self.rect = self.image.get_rect(topleft=pos)
