import math
import pygame

WIDTH = 1200
HEIGHT = 800

BLACK = (0, 0, 0)
DARK_GRAY = (169, 169, 169)

FPS = 165

MOVE_BUTTONS_PRESS = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False,
                      pygame.K_q: False, pygame.K_e: False}  # зажатые клавиши

SPEED = 2

start_player_pos = (WIDTH // 2, HEIGHT // 2)
player_view = 3 * math.pi / 2  # направление взгляда игрока (тригонометрический круг), изначально вверх

FOV = math.pi / 3 # угол обзора
RAYS_INT = 100
DRAWING_RANGE = 800 # дальность прорисовки
DELTA_ANGEL = FOV / RAYS_INT # углы между лучами

TurningSpeed = 0.01

WALL_SIZE = 100