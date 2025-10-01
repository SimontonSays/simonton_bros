# level.py
import pygame
from settings import TILESIZE
from tiles import Tile
from player import Player

class Level:
    def __init__(self, level_lines):
        self.all_sprites = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.player = None

        for r, line in enumerate(level_lines):
            for c, ch in enumerate(line.rstrip("\n")):
                x, y = c * TILESIZE, r * TILESIZE
                if ch == "X":
                    t = Tile((x, y), "block")
                    self.solids.add(t); self.all_sprites.add(t)
                elif ch == "G":
                    t = Tile((x, y), "ground")
                    self.solids.add(t); self.all_sprites.add(t)
                elif ch == "P":
                    self.player = Player((x, y - TILESIZE // 2))

        if self.player is None:
            self.player = Player((TILESIZE * 2, TILESIZE * 2))
        self.all_sprites.add(self.player)

    def update(self):
        self.player.update(self.solids)

    def draw(self, surface, offset):
        ox, oy = int(offset[0]), int(offset[1])
        for s in self.all_sprites:
            surface.blit(s.image, (s.rect.x - ox, s.rect.y - oy))
