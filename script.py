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
snake_vel = 2
fps = 10


#Sonds effects
pygame.mixer.init() 
weee = pygame.mixer.Sound(r"Assets/weee.mp3")
windows_xp = pygame.mixer.Sound(r"Assets/windows_xp.mp3")
classic_hurt = pygame.mixer.Sound(r"Assets/classic_hurt.mp3")
horn = pygame.mixer.Sound(r"Assets/horn.mp3")
windows_xp2 = pygame.mixer.Sound("Assets/windows_xp2.mp3") 
eating = pygame.mixer.Sound(r"Assets/eating.mp3")
themeSong = pygame.mixer.Sound(r"Assets/ThemeSong.mp3")
themeSong.play(-1)

font = pygame.font.Font('freesansbold.ttf', 20)
death_font = pygame.font.Font('freesansbold.ttf', 32)

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Snake game')


class Snake():
    def __init__(self, snake_size, snake_color, snake_vel, tail_color, x, y):
        self.size = snake_size
        self.color = snake_color
        self.vel = snake_vel
        self.tail_color = tail_color        
        self.x = x
        self.y = y

    def draw(self):
        snake = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(win, self.color, snake)

    def move(self, keys_pressed):
        lost = False
        self.last_movement = (self.x, self.y)

        if keys_pressed["left"]:
            if self.x - snake_vel < 0:
                lost = True
            else:
                self.x -= snake_size

        if keys_pressed["right"]:
            if self.x + snake_vel + 20 > width:
                lost = True
            else:
                self.x += snake_size

        if keys_pressed["up"]:
            if self.y - snake_vel < 0:
                lost = True
            else:
                self.y -= snake_size

        if keys_pressed["down"]:
            if self.y + snake_vel + 20 > heigth:
                lost = True
            else:
                self.y += snake_size

        return self.x, self.y, lost

    def draw_tails(self,tails):
        for i in tails:
            tail = pygame.Rect(i[0], i[1], self.size, self.size)
            pygame.draw.rect(win, tail_color, tail)


    def handle_colision(self, apple_x, apple_y):
        apple = pygame.Rect(apple_x, apple_y, 10, 10)
        snake = pygame.Rect(self.x, self.y, self.size, self.size)

        if apple.colliderect(snake):
            return True
        return False


    def move_tails(pos, tails):
        new_tails = []
        for tail in tails:
            new_tails.append(pos)
            pos = tail
        return new_tails

#Handles the key presses by turning the apopriate value to true and others to false 
def handle_keys(key, keys_pressed, key_history):
    if key == K_LEFT or key == K_a:#Left Arrow
        for key in keys_pressed: 
            keys_pressed[key] = False
        keys_pressed["left"] = True 
        key_history.append("left")

    if key == K_RIGHT or key == K_d:#Right Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["right"] = True
        key_history.append("right")

    if key == K_UP or key == K_w:#Up Arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["up"] = True
        key_history.append("up")

    if key == K_DOWN or key == K_s:#Down arrow
        for key in keys_pressed:
            keys_pressed[key] = False
        keys_pressed["down"] = True
        key_history.append("down")

    return key_history

def generate_apples():
    x = random.randint(1, width - 1)
    y = random.randint(1, heigth - 1)
    return x, y


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




def main():
    x, y = width//2 - 10, heigth//2 - 10#The x and y of the snake
    snake = Snake(snake_size, snake_color, snake_vel, tail_color, x, y)
    score = 0
    tails, key_history = [], []

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
                key_history = handle_keys(event.key, keys_pressed, key_history)
                
        if run:
            snake.draw() 
            snake.draw_tails(tails)
            x, y, lost = snake.move(keys_pressed)
            tails = snake.move_tails(tails)

            if no_apple:
                apple_x, apple_y = generate_apples()
                no_apple = False

            pygame.draw.circle(win, (255, 0, 0), (apple_x, apple_y), 10)#Draws the apple's
            no_apple = snake.handle_colision(apple_x, apple_y)

            if no_apple == True:#The snake colided with the apple
                eating.play()
                score += 1
                tails.append(last_movement)
            display_points(score)

            for tail in tails:
                if x == tail[0] and y == tail[1]:
                    lost = True
                    break

            if lost:
                themeSong.stop()
                high_score = get_high_score(score)
                play_sound()
                display_death_message(score, high_score)
                run = False
                break

            pygame.display.update()
            win.fill(black)#fills the background color
     
if __name__ == '__main__':
    main()
