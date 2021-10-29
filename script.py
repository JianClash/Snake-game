import pygame

pygame.init()
width, heigth = 1300, 700

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Snake game')


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break

main()