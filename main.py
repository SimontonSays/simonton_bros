import clock
import pygame, sys



import level
from settings import WIDTH, HEIGHT, FPS, SKY_BLUE, TITLE
from level import Level

def load_level_text(path):
    with open(path, "r") as f:
        return f.read().splitlines()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simonton Bros")
    clock = pygame.time.Clock()

    try:
        level_lines = load_level_text("assets/levels/level1.txt")
    except FileNotFoundError:
        print(">>> assets/levels/level1.txt not found; using fallback map")
        level_lines = [
            "....................................",
            "....................................",
            "..............XXX...................",
            "....................................",
            "..........P.........................",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        ]

    level = Level(level_lines)
    camera = pygame.math.Vector2(0, 0)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Update world
        level.update()

        #Center camera on player
        # Center camera on player
        camera.x = level.player.rect.centerx - WIDTH // 2
        camera.y = level.player.rect.centery - HEIGHT // 2

        #Draw
        screen.fill(SKY_BLUE)  # sky blue background
        level.draw(screen, camera)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
