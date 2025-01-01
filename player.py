from settings import *
import pygame


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.view = player_view

    def move(self):
        pressed_keys = [key for key, keydown_bool in MOVE_BUTTONS_PRESS.items() if keydown_bool]  # зажатые клавиши
        full_speed = len(pressed_keys) != 2 # чтобы игрок наискось не двигался в 2 раза быстрее
        if full_speed:
            pos_change = speed
        else:
            pos_change = speed / 2
        # изменение координат
        for direction in pressed_keys:
            if direction == "w":
                self.y -= pos_change
            elif direction == "a":
                self.x -= pos_change
            elif direction == "s":
                self.y += pos_change
            elif direction == "d":
                self.x += pos_change
