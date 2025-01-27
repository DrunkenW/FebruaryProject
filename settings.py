import math
import pygame

# размеры окна
WIDTH = 1920
HEIGHT = 1080

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)

FPS = 165
MAX_FPS = 100

MOVE_SPEED = 1

start_player_pos = (WIDTH // 2, HEIGHT // 2)
player_angle = 0
player_speed = 2

WALL_SIZE = 100

FOV = math.pi / 3  # угол обзора
RAYS_INT = 320
DRAWING_RANGE = 800  # дальность прорисовки
DELTA_ANGLE = FOV / RAYS_INT  # углы между лучами
DIST = RAYS_INT // (2 * math.tan(FOV / 2))
PROJ_COEF = 3 * DIST * WALL_SIZE

TurningSpeed = 0.015  # скорость поворота

# texture настройки
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // WALL_SIZE

# sprites
SPRITE_SIZE = 100

#оружие параметры спрайтов

WEAPON_WIDTH = 400
WEAPON_HEIGHT = 300

DOUBLE_PI = math.pi * 2
CENTER_RAY = RAYS_INT // 2 - 1
FAKE_RAYS = 100
HALF_FOV = FOV / 2
SCALE = WIDTH // RAYS_INT


MOUSE_SENSITIVITY = 0.001  # Чувствительность мыши (можно регулировать)

SOUNDS = {
    'shotgun': 'sounds/dsdshtgn.mp3',
    'background': 'sounds/background.mp3'
}