import random
import pygame
import sys
from pygame.locals import *


# Функция отрисовки света фонаря
def isLighted(tile, tileRow, tileColumn, player):
    if (tileRow - player[0]) ** 2 + (tileColumn - player[1]) ** 2 <= 8:
        return tile
    else:
        return DARKNESS


# Функции проверки движений
def isTopOkay(objectToMove, direction):
    if objectToMove[0] + direction[0] < 0:
        return False
    else:
        return True


def isBotOkay(objectToMove, direction):
    if objectToMove[0] + direction[0] >= MAPHEIGHT:
        return False
    else:
        return True


def isLeftOkay(objectToMove, direction):
    if objectToMove[1] + direction[1] < 0:
        return False
    else:
        return True


def isRightOkay(objectToMove, direction):
    if objectToMove[1] + direction[1] >= MAPWIDTH:
        return False
    else:
        return True


# Функция поднятия топора
def isAxeInHand(player, axe):
    if player[0] == axe[0] and player[1] == axe[1]:
        print("You picked up the axe!")
        player[3] = True
    return player


# Функция перемещения
def moveIntoDirection(objectToMove, direction):
    objectToMove[0] += direction[0]
    objectToMove[1] += direction[1]
    return objectToMove


# Функция отрисовки движения
def moveEntity(entity, direction):
    tilemap[entity[0]][entity[1]] = LIGHT
    entity = moveIntoDirection(entity, direction)
    tilemap[entity[0]][entity[1]] = entity[2]
    return entity


# Отрисовываем текущее значение карты
def drawMap():
    # Отрисовываем топор, если на него шагнули и еще не подобрали
    if playerInfo[3] is False and (tigerInfo[0] != axeInfo[0] or tigerInfo[1] != axeInfo[1]):
        tilemap[axeInfo[0]][axeInfo[1]] = axeInfo[2]
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            pygame.draw.rect(DISPLAYSURF, colors[isLighted(tilemap[row][column], row, column, playerInfo)], (column * TILESIZE + column, row * TILESIZE + row, TILESIZE, TILESIZE))


# Проверяем, закончилась ли игра
def isGameNotOver(tiger, victim):
    if tiger[0] == victim[0] and tiger[1] == victim[1]:
        if victim[3]:
            print("You defeated the tiger!")
        else:
            print("Tiger killed You(")
        return False
    else:
        return True


# Логика тигра
def tigerLogic(tiger, victim):
    action = list()
    if tiger[1] != victim[1]:
        if tiger[1] - victim[1] > 0:
            action.append(LEFT)
        else:
            action.append(RIGHT)
    if tiger[0] != victim[0]:
        if tiger[0] - victim[0] > 0:
            action.append(UP)
        else:
            action.append(DOWN)
    if action:
        tiger = moveEntity(tiger, random.choice(action))
    return tiger


# Задаем константы перемещений
UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)


# Задаем цвета тайлов
BLACK = (50, 50, 50)
GRAY = (150, 150, 150)
METALLIC = (200, 200, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Задаем константы для каждого тайла
DARKNESS = 0
PLAYER = 1
TIGER = 2
LIGHT = 3
AXE = 4

# Задаем словарь для соотношения цветов и тайлов
colors = {
    DARKNESS: BLACK,
    PLAYER: YELLOW,
    TIGER: ORANGE,
    LIGHT: GRAY,
    AXE: METALLIC
}

TILESIZE = 60  # Размер одного тайла
MAPWIDTH = 20  # Ширина карты в тайлах
MAPHEIGHT = 15  # Высота карты в тайлах

tilemap = list(list(LIGHT for tileRow in range(MAPWIDTH)) for tileColumn in range(MAPHEIGHT))

playerInfo = list((random.randint(0, 2), random.randint(0, 2), PLAYER, False))
tigerInfo = list((random.randint(10, 14), random.randint(0, 4), TIGER))
axeInfo = list((random.randint(4, 10), random.randint(11, 17), AXE))

tilemap[playerInfo[0]][playerInfo[1]] = playerInfo[2]
tilemap[tigerInfo[0]][tigerInfo[1]] = tigerInfo[2]
tilemap[axeInfo[0]][axeInfo[1]] = axeInfo[2]

# Инициализируем дисплей и карту
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * (TILESIZE + 1), MAPHEIGHT * (TILESIZE + 1)))
drawMap()
pygame.display.update()

# Сессия игры
while isGameNotOver(tigerInfo, playerInfo):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if isTopOkay(playerInfo, UP):
                    playerInfo = moveEntity(playerInfo, UP)
                tigerInfo = tigerLogic(tigerInfo, playerInfo)
                playerInfo = isAxeInHand(playerInfo, axeInfo)
            if event.key == pygame.K_DOWN:
                if isBotOkay(playerInfo, DOWN):
                    playerInfo = moveEntity(playerInfo, DOWN)
                tigerInfo = tigerLogic(tigerInfo, playerInfo)
                playerInfo = isAxeInHand(playerInfo, axeInfo)
            if event.key == pygame.K_RIGHT:
                if isRightOkay(playerInfo, RIGHT):
                    playerInfo = moveEntity(playerInfo, RIGHT)
                tigerInfo = tigerLogic(tigerInfo, playerInfo)
                playerInfo = isAxeInHand(playerInfo, axeInfo)
            if event.key == pygame.K_LEFT:
                if isLeftOkay(playerInfo, LEFT):
                    playerInfo = moveEntity(playerInfo, LEFT)
                tigerInfo = tigerLogic(tigerInfo, playerInfo)
                playerInfo = isAxeInHand(playerInfo, axeInfo)
            if event.key == pygame.K_SPACE:
                tigerInfo = tigerLogic(tigerInfo, playerInfo)
    drawMap()
    pygame.display.update()
