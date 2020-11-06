import pygame
import random
import math
from pygame import mixer

# initializing
pygame.init()

# create the screen
screen = pygame.display.set_mode((600, 400))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player.png")
player_x = 255
player_y = 250
player_x_change = 0

# enemy
enemyImg = pygame.image.load("enemy.png")
enemy_x = random.randint(0, 600)
enemy_y = random.randint(10, 50)
enemy_x_change = 0.2
enemy_y_change = 30

# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 250
bullet_x_change = 0
bullet_y_change = 0.4
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 150))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 25:
        return True
    else:
        return False


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.4
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # background color
    screen.fill((0, 0, 0))

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 536:
        player_x = 536

    enemy_x += enemy_x_change

    if enemy_x <= 0:
        enemy_x_change = 0.2
        enemy_y += enemy_y_change
    elif enemy_x >= 536:
        enemy_x_change = -0.2
        enemy_y += enemy_y_change
    if enemy_y > 210:
        enemy_y = 2000
        game_over()

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 250
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    # collision
    col = collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if col:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        bullet_y = 250
        bullet_state = "ready"
        score_value += 1
        enemy_x = random.randint(0, 536)
        enemy_y = random.randint(10, 50)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(text_x, text_y)
    pygame.display.update()
