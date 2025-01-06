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
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)


FPS = 165
MAX_FPS = 100
BUTTONS_PRESS = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False, pygame.K_q: False,
                 pygame.K_e: False}  # зажатые клавиши, q и e - поворот камеры

MOVE_SPEED = 1

start_player_pos = (WIDTH // 3, HEIGHT // 3)
player_direction_of_view = 3 * math.pi / 2  # направление взгляда игрока (тригонометрический круг), изначально вверх

WALL_SIZE = 100

FOV = math.pi / 3  # угол обзора
RAYS_INT = 120
DRAWING_RANGE = 800  # дальность прорисовки
DELTA_ANGLE = FOV / RAYS_INT  # углы между лучами
DIST = RAYS_INT // (2 * math.tan(FOV / 2))
PROJ_COEF = 3 * DIST * WALL_SIZE
SCALE = WIDTH // RAYS_INT

TurningSpeed = 0.01  # скорость поворота

player_angle = 0
player_speed = 2
