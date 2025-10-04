# player.py
import os

import pygame
from settings import TILESIZE, GRAVITY, RUN_SPEED, JUMP_VELOCITY, PLAYER_GREEN

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load sprite
        project_root = os.path.dirname(os.path.abspath(__file__))
        sprite_path = os.path.join(project_root, "assets", "sprites", "player.png")
        print(f"[PLAYER] CWD={os.getcwd()}")
        print(f"[PLAYER] Expecting sprite: {sprite_path}  (exists? {os.path.exists(sprite_path)})")

        try:
            img = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.smoothscale(img, (int(TILESIZE * 0.9), int(TILESIZE * 0.95)))
            print("[PLAYER] Sprite loaded OK")
        except Exception as e:
            print(f"[PLAYER] FALLBACK to green block. Reason: {repr(e)}")
            self.image = pygame.Surface((int(TILESIZE * 0.8), int(TILESIZE * 0.95)), pygame.SRCALPHA)
            self.image.fill(PLAYER_GREEN)
        self.rect = self.image.get_rect(topleft=pos)

        # Movement state
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.coyote_frames = 0   # grace frames after leaving ground
        self.jump_buffer = 0     # grace frames after pressing jump

    def _input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -RUN_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = RUN_SPEED
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump_buffer = 6

    def _apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 18:
            self.vel.y = 18

    def _try_jump(self):
        if (self.on_ground or self.coyote_frames > 0) and self.jump_buffer > 0:
            self.vel.y = JUMP_VELOCITY
            self.on_ground = False
            self.coyote_frames = 0
            self.jump_buffer = 0

    def _collide_axis(self, solids, axis):
        for tile in solids:
            if self.rect.colliderect(tile.rect):
                if axis == "x":
                    if self.vel.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = tile.rect.right
                else:  # axis == 'y'
                    if self.vel.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                        self.coyote_frames = 6
                    elif self.vel.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.vel.y = 0

    def update(self, solids):
        self._input()
        self._apply_gravity()
        self._try_jump()

        self.rect.x += int(self.vel.x)
        self._collide_axis(solids, "x")

        # assume airborne until proven grounded
        was_grounded = self.on_ground
        self.on_ground = False

        self.rect.y += int(self.vel.y)
        self._collide_axis(solids, "y")

        if not self.on_ground and self.coyote_frames > 0:
            self.coyote_frames -= 1
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
