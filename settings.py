import math
import pygame

# размеры окна
WIDTH = 1920
HEIGHT = 1080

BLACK = (0, 0, 0)
DARK_GRAY = (169, 169, 169)
WHITE = (255, 255, 255)

FPS = 165

BUTTONS_PRESS = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False, pygame.K_q: False,
                 pygame.K_e: False}  # зажатые клавиши, q и e - поворот камеры

MOVE_SPEED = 1

start_player_pos = (WIDTH // 2, HEIGHT // 2)
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
