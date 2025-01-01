from math import pi
import pygame

WIDTH = 1000
HEIGHT = 800

BLACK = (0, 0, 0)

MOVE_BUTTONS = {pygame.K_w: "w", pygame.K_a: "a", pygame.K_s: "s", pygame.K_d: "d"}
MOVE_BUTTONS_PRESS = {"w": False, "a": False, "s": False, "d": False}  # зажатые клавиши

speed = 2

player_pos = (WIDTH // 2, HEIGHT // 2)
player_view = pi / 2  # взгляд игрока (тригонометрический круг)
