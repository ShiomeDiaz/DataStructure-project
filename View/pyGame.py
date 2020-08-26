import pygame
pygame.init()
size = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("prueba")
run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

pygame.quit()
