import math
import pygame

WIDTH = 1000
HEIGHT = 800

BLACK = (0, 0, 0)

FPS = 165

MOVE_BUTTONS_PRESS = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False,
                      pygame.K_q: False, pygame.K_e: False}  # зажатые клавиши

speed = 2

start_player_pos = (WIDTH // 2, HEIGHT // 2)
player_view = 3 * math.pi / 2  # направление взгляда игрока (тригонометрический круг), изначально вверх

TurningSpeed = 0.01
