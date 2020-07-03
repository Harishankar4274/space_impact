import random
import math
import pygame
from pygame import mixer

# initializing the pygame

pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Backgroung image
background = pygame.image.load('space_bg.jpeg')

# Backgound Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 20
# Bullet state: Ready == can't be seen ; Fire == moving
bullet_state = "ready"

# Score
score = 0
total_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score :" + str(total_score), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))

# Bullet Collision
def bullet_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Spaceship Collision
def ship_collision(enemyX, enemyY, playerX, playerY):
    enemy_distance = math.sqrt((math.pow((enemyX - playerX), 2)) + (math.pow((enemyY - playerY), 2)))
    if enemy_distance < 27:
        return True

def player(x, y):
    screen.blit(player_img, (playerX, playerY))


# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,50))
    enemyX_change.append(2)
    enemyY_change.append(20)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Firing Bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16 , y + 10))

# Game Loop. All the game functions will run in this loop.
running = True
while running:
    pygame.display.update()
    # Screen BackGround in RGB
    screen.fill((10, 0, 50))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement of the spaceship/checking the keystroke for direction.
        if event.type == pygame.KEYDOWN:
            # Key pressed
            # X axis
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            # Y axis
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

            # Firing bullets
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            # Key Released
            playerY_change = 0
            playerX_change = 0

    # Movement of Spaceship
    playerX += playerX_change
    # making the horizontal boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerY += playerY_change
    # making the vertical boundaries
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    playerY += playerY_change

# Bullet Movement
    # bullet reload
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    # bullet fire
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling player ship
    player(playerX, playerY)

    # movement of the enemy/checking for the boundaries
        # X axis
    #if enemyX <= 0:
    #    enemyX = 0
    #if enemyX >= 736:
    #    enemyX = 730

        # Y axis
    #if enemyY <= 0:
    #   enemyY = 0
    #if enemyY >= 536:
    #   enemyY = 0

    # Movement of enemy
    for i in range(num_of_enemy):

        # Game Over
        attack = ship_collision(enemyX[i], enemyY[i], playerX, playerY)
        if attack:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # moving enemy horizontally
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # If Collision Happened
        collision = bullet_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score += 1
            if score == 5:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                total_score += score
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 50)
                score = 0

        # calling enemy
        enemy(enemyX[i], enemyY[i], i)

    #Displaying Score
    show_score(textX, textY)
    #pygame.display.update()
