import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP

pygame.init()
width, heigth = 1300, 700

snake_color = (0, 30, 150)
black = (0, 0, 0)

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Snake game')

def draw_snake(x, y):
    snake = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(win, snake_color, snake)

#Moves the snake by updating the x and y values
def move_snake(x, y, left, right, up, down):
    if left:
        x -= 1
    if right:
        x += 1
    if up:
        y -= 1
    if down:
        y += 1

    return x, y

#Handles the key presses by turning the apopriate value to true and others to false 
def handle_keys(key, keys_pressed):
    if key == K_LEFT:#Left Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["left"] = True 

    if key == K_RIGHT:#Right Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["right"] = True

    if key == K_UP:#Up Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["up"] = True

    if key == K_DOWN:#Down arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["down"] = True

def main():
    x, y = width//2, heigth//2 #The x and y of the snake
    keys_pressed = {"left":False, "right":False, "up":False, "down":False}#the values that will turn True when the apopriate key is pressed
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break
            if event.type == pygame.KEYDOWN:
                handle_keys(event.key, keys_pressed)
                
        if run:
            draw_snake(x, y)
            x, y = move_snake(x, y, keys_pressed["left"], keys_pressed["right"], keys_pressed["up"], keys_pressed["down"])
            pygame.display.update()
            win.fill(black)#fills the background color
            
main()