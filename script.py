import pygame, random
from pygame import display
from pygame import time
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w
from pygame.rect import Rect

pygame.init()
width, heigth = 1300, 700

snake_color = (144,238,144)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

snake_size = 20
vel = 2
fps = 80
font = pygame.font.Font('freesansbold.ttf', 20)
death_font = pygame.font.Font('freesansbold.ttf', 32)

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Snake game')

def draw_snake(x, y, points):
    # if points != 0:
    #     snake = pygame.Rect(x, y, 20 * points, 20)
    # else:
    snake = pygame.Rect(x, y, snake_size, snake_size)
    pygame.draw.rect(win, snake_color, snake)

#Moves the snake by updating the x and y values
def move_snake(x, y, left, right, up, down, points):
    lost = False
    if left:
        if x - vel < 0:
            lost = True
        else:
            x -= vel

    if right:
        if x + vel + 20 > width:
            print("b")
            lost = True
        else:
            x += vel

    if up:
        if y - vel < 0:
            lost = True
        else:
            y -= vel

    if down:
        if y + vel + 20 > heigth:
            lost = True
        else:
            y += vel

    return x, y, lost

#Handles the key presses by turning the apopriate value to true and others to false 
def handle_keys(key, keys_pressed):
    if key == K_LEFT or key == K_a:#Left Arrow
        for key in keys_pressed: 
            keys_pressed[key] = False
        keys_pressed["left"] = True 

    if key == K_RIGHT or key == K_d:#Right Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["right"] = True

    if key == K_UP or key == K_w:#Up Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["up"] = True

    if key == K_DOWN or key == K_s:#Down arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["down"] = True

def generate_apples():
    x = random.randint(1, width - 1)
    y = random.randint(1, heigth - 1)
    return x, y

def handle_colision(apple_x, apple_y, x, y):
    apple = pygame.Rect(apple_x, apple_y, 10, 10)
    snake = pygame.Rect(x, y, 20, 20)

    if apple.colliderect(snake):
        return True
    return False

def display_points(points):
    text = font.render(f"Score: {points}", True, white)
    textRect = text.get_rect()
    textRect.center = (50, 20)
    win.blit(text, textRect)

def draw_lines():
    for i in range(width//snake_size):
        pygame.draw.line(win, white, (snake_size*i, 0), (snake_size*i, heigth*i))

    for i in range(heigth//snake_size):
        pygame.draw.line(win, white, (0, snake_size*i), (width, snake_size*i))

def display_death_message():
    text = death_font.render("You died!!!", True, red)
    textRect = text.get_rect()
    textRect.center = (width//2, heigth//2)
    win.blit(text, textRect)
    pygame.display.update()
    time.wait(5000)

def main():
    x, y = width//2 - 10, heigth//2 - 10#The x and y of the snake
    points = 0

    keys_pressed = {"left":False, "right":False, "up":False, "down":False}#the values that will turn True when the apopriate key is pressed
    no_apple, run, lost = True, True, False

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
            draw_lines()
            draw_snake(x, y, points)
            x, y, lost = move_snake(x, y, keys_pressed["left"], keys_pressed["right"], keys_pressed["up"], keys_pressed["down"], points)

            if no_apple:
                apple_x, apple_y = generate_apples()
                no_apple = False

            pygame.draw.circle(win, (255, 0, 0), (apple_x, apple_y), 10)#Draws the apple's
            no_apple = handle_colision(apple_x, apple_y, x, y)

            if no_apple == True:#The snake colided with the apple increase the ponints by 1
                points += 1
            display_points(points)

            if lost:
                display_death_message()
                run = False
                break

            pygame.display.update()
            win.fill(black)#fills the background color
            
main()