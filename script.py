import pygame, random
from pygame import time
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w

pygame.init()
width, heigth = 1300, 700

snake_color = (0,255,0)
tail_color = (0,255,0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

snake_size = 20
vel = 2
fps = 10

pygame.mixer.init()
weee = pygame.mixer.Sound(r"assets/weee.mp3")
windows_xp = pygame.mixer.Sound(r"assets/windows_xp.mp3")
classic_hurt = pygame.mixer.Sound(r"assets/classic_hurt.mp3")
horn = pygame.mixer.Sound(r"assets/horn.mp3")
windows_xp2 = pygame.mixer.Sound("assets/windows_xp2.mp3") 
eating = pygame.mixer.Sound(r"assets/eating.mp3")

bg = pygame.image.load(r"assets/snakeBackground.png")
bg = pygame.transform.scale(bg, (width, heigth))

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
    last_movement = (x, y)
    lost = False
    if left:
        if x - vel < 0:
            lost = True
        else:
            x -= snake_size

    if right:
        if x + vel + 20 > width:
            lost = True
        else:
            x += snake_size

    if up:
        if y - vel < 0:
            lost = True
        else:
            y -= snake_size

    if down:
        if y + vel + 20 > heigth:
            lost = True
        else:
            y += snake_size

    return x, y, lost, last_movement

#Handles the key presses by turning the apopriate value to true and others to false 
def handle_keys(key, keys_pressed):
    if key == K_LEFT or key == K_a:#Left Arrow
        last_input = "left"
        for key in keys_pressed: 
            keys_pressed[key] = False
        keys_pressed["left"] = True 

    if key == K_RIGHT or key == K_d:#Right Arrow
        last_input = "right"
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["right"] = True

    if key == K_UP or key == K_w:#Up Arrow
        last_input = "up"
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["up"] = True

    if key == K_DOWN or key == K_s:#Down arrow
        last_input = "down"
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["down"] = True

    return last_input

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

def display_death_message(score, high_score):
    text = death_font.render(f"Your score:{score}", True, red)
    textRect = text.get_rect()
    textRect.center = (width//2, heigth//2)
    win.blit(text, textRect)

    highScoreText = death_font.render(f"High score:{high_score}", True, red)
    highScoreTextRect = highScoreText.get_rect()
    highScoreTextRect.center = (width//2, heigth//2 + 30)
    win.blit(highScoreText, highScoreTextRect)
    pygame.display.update()
    time.wait(5000)

def play_sound():
    num = random.randint(1, 5)
    if num == 1:
        weee.play()
    elif num == 2:
        classic_hurt.play()
    elif num == 3:
        horn.play()
    elif num == 4:
        windows_xp2.play()
    else:
        windows_xp.play()

def get_high_score(score):
    with open("high_score.txt", "r") as file:
        high_score = file.read()

    if int(high_score) < score:
        file = open("high_score.txt", "w")
        file.write(str(score))
        high_score = score
        file.close()

    return int(high_score)

def draw_tails(tails):
    for i in tails:
        tail = pygame.Rect(i[0], i[1], snake_size, snake_size)
        pygame.draw.rect(win, tail_color, tail)

def move_tails(pos, tails):
    new_tails = []
    for tail in tails:
        new_tails.append(pos)
        pos = tail

    return new_tails


def main():
    x, y = width//2 - 10, heigth//2 - 10#The x and y of the snake
    score = 0
    tails = []

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
            win.blit(bg, (0, 0))
            draw_snake(x, y, score)
            draw_tails(tails)
            x, y, lost, last_movement = move_snake(x, y, keys_pressed["left"], keys_pressed["right"], keys_pressed["up"], keys_pressed["down"], score)
            tails = move_tails((last_movement), tails)

            if no_apple:
                apple_x, apple_y = generate_apples()
                no_apple = False

            pygame.draw.circle(win, (255, 0, 0), (apple_x, apple_y), 10)#Draws the apple's
            no_apple = handle_colision(apple_x, apple_y, x, y)

            if no_apple == True:#The snake colided with the apple increase the ponints by 1
                eating.play()
                score += 1
                tails.append(last_movement)
            display_points(score)

            for tail in tails:
                if x == tail[0] and y == tail[1]:
                    lost = True
                    break

            if lost:
                high_score = get_high_score(score)
                play_sound()
                display_death_message(score, high_score)
                run = False
                break

            
            pygame.display.update()
            win.fill(black)#fills the background color
            
main()