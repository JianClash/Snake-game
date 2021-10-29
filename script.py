import pygame, random
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP

pygame.init()
width, heigth = 1300, 700

snake_color = (144,238,144)
black = (0, 0, 0)

fps = 60
font = pygame.font.Font('freesansbold.ttf', 32)

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Snake game')

def draw_snake(x, y):
    snake = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(win, snake_color, snake)

#Moves the snake by updating the x and y values
def move_snake(x, y, left, right, up, down):
    if left:
        x -= 3
    if right:
        x += 3
    if up:
        y -= 3
    if down:
        y += 3

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

def generate_apples():
    x = random.randint(0, width)
    y = random.randint(0, heigth)
    return x, y

def handle_colision(apple_x, apple_y, x, y):
    apple = pygame.Rect(apple_x, apple_y, 10, 10)
    snake = pygame.Rect(x, y, 20, 20)

    if apple.colliderect(snake):
        return True
    return False

def display_points(points):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f"eatan: {points}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (50, 20)
    win.blit(text, textRect)

def main():
    x, y = width//2, heigth//2 #The x and y of the snake
    points = 0

    keys_pressed = {"left":False, "right":False, "up":False, "down":False}#the values that will turn True when the apopriate key is pressed
    no_apple, run = True, True

    clock = pygame.time.Clock()

    while run:
        clock.tick_busy_loop(fps)
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
            
            if no_apple:
                apple_x, apple_y = generate_apples()
                no_apple = False
            pygame.draw.circle(win, (255, 0, 0), (apple_x, apple_y), 10)#Draws the apple's
            no_apple = handle_colision(apple_x, apple_y, x, y)

            if no_apple == True:#The snake colided with the apple increase the ponints by 1
                points += 1
            display_points(points)

            pygame.display.update()
            win.fill(black)#fills the background color
            
main()