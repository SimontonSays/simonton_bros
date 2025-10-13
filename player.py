# player.py
import os

import pygame
from settings import TILESIZE, GRAVITY, RUN_SPEED, JUMP_VELOCITY, PLAYER_GREEN

def load_scaled(path, size):
    """Load a PNG with alpha and scale to (w, h). Raises if not found."""
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load sprite
        project_root = os.path.dirname(os.path.abspath(__file__))
        sprite_path = os.path.join(project_root, "assets", "sprites")
        print(f"[PLAYER] CWD={os.getcwd()}")
        print(f"[PLAYER] Expecting sprite: {sprite_path}  (exists? {os.path.exists(sprite_path)})")

        target_size = (int(TILESIZE * 0.9), int(TILESIZE * 0.95))

        # Load frames (with fallbacks)
        def try_load(name):
            p = os.path.join(sprite_path, name)
            if os.path.exists(p):
                return load_scaled(p, target_size)
            return None

        #Load frames
        idle = try_load("player_idle.png")
        walk1 = try_load("player_walk1.png")
        walk2 = try_load("player_walk2.png")
        jump = try_load("player_jump.png")
        base = None
        if not any([idle, walk1, walk2, jump]):
            # last resort: player.png
            base_path = try_load("player.png")
            if base_path:
                base = base_path

        # If nothing found at all, make a green block so the game never crashes
        if not any([idle, walk1, walk2, jump, base]):
            print("[PLAYER] No sprite images found; using green rectangle")
            base = pygame.Surface(target_size, pygame.SRCALPHA)
            base.fill(PLAYER_GREEN)

        # Build animation sets with sensible fallbacks
        self.frames = {
            "idle": [idle or base],
            "walk": [f for f in (walk1, walk2) if f] or [base, base],
            "jump": [jump or base],
        }

        # Current image (start idle)
        self.state = "idle"
        self.frame_index = 0
        self.image = self.frames[self.state][self.frame_index]

        # Precompute left/right versions for fast flipping
        self.right_sets = {k: v[:] for k, v in self.frames.items()}
        self.left_sets = {k: [pygame.transform.flip(f, True, False) for f in v]
                          for k, v in self.frames.items()}
        self.facing = 1  # 1 = right, -1 = left

        self.rect = self.image.get_rect(topleft=pos)

        # Movement state
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.coyote_frames = 0   # grace frames after leaving ground
        self.jump_buffer = 0     # grace frames after pressing jump

        # Animation timing
        self.walk_switch_ms = 120  # time between walk frames
        self.last_switch = pygame.time.get_ticks()

    def _input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -RUN_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = RUN_SPEED
            self.facing = 1
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

    # Animation
    def _pick_state(self):
        if not self.on_ground:
            return "jump"
        if abs(self.vel.x) > 0:
            return "walk"
        return "idle"

    def _animate(self):
        now = pygame.time.get_ticks()
        new_state = self._pick_state()

        # Reset animation after state changes
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.last_switch = now

        # Advance frames for walk animation
        if self.state == "walk" and now - self.last_switch >= self.walk_switch_ms:
            self.frame_index = (self.frame_index + 1) % len(self.frames["walk"])
            self.last_switch = now

        # Choose correct facing set & keep feet planted
        bottomleft = self.rect.bottomleft
        set_for_dir = self.right_sets if self.facing == 1 else self.left_sets
        frames = set_for_dir[self.state]
        self.image = frames[self.frame_index % len(frames)]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft

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

        self._animate()
