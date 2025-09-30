import pygame, sys

pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simonton Bros")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((140, 200, 255))  # sky blue background
    pygame.display.flip()
    clock.tick(60)
