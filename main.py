import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_RIGHT, K_LEFT, K_UP

pygame.init()
pygame.mixer.init() #music

# title
pygame.display.set_caption("Гусак Бандера")

HEIGHT = 600
WIDTH = 1000

# music
pygame.mixer.music.load('music\\mario.ogg')
pygame.mixer.music.play()

FONT = pygame.font.SysFont('Verdana', 30)
FPS = pygame.time.Clock()

COLOR_DIAMONDBLUE = (62, 95, 138)
COLOR_YELLOW = (255,176,46)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0, 0, 255)
COLOR_GEEN = (50, 205, 50)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('img\\background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# player animation
IMAGE_PATH = "img\\goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (120, 60)

player = pygame.transform.scale(pygame.image.load('img\\player.png').convert_alpha(), (120, 60))
player_rect = player.get_rect(topleft=(0, HEIGHT/2))

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]

def create_enemy():
    enemy_size = (102, 36)
    enemy = pygame.transform.scale(pygame.image.load('img\\enemy.png').convert_alpha(), (102, 36))
   # enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT - enemy.get_height()),*enemy.get_size())
    enemy_rect = pygame.Rect(WIDTH, random.randint(HEIGHT/5, HEIGHT/5*4), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (90, 100)
    bonus = pygame.transform.scale(pygame.image.load('img\\bonus.png').convert_alpha(), (90, 100))
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []
score = 0


image_index = 0

playing = True
while playing:
    FPS.tick(140)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])), (120, 60))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
   
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < - bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < - bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])

        if player_rect.colliderect(bonus[1]):
            pygame.mixer.music.load('music\\scoreplus.ogg')
            pygame.mixer.music.play()
            score += 1
            bonuses.pop(bonuses.index(bonus))

   
    main_display.blit(FONT.render(str(score), True, COLOR_DIAMONDBLUE), (WIDTH/2, 20))
    main_display.blit(player, (player_rect))
    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))