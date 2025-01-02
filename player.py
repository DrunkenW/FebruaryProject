from settings import *


class Player:
    def __init__(self):
        self.x, self.y = start_player_pos
        self.view = player_view

    def pos(self):
        return self.x, self.y

    def move(self):
        pressed_keys = [key for key, keydown_bool in MOVE_BUTTONS_PRESS.items() if keydown_bool]  # зажатые клавиши
        full_speed = len(pressed_keys) != 2  # чтобы игрок наискось не двигался в 2 раза быстрее
        if full_speed:
            pos_change = SPEED
        else:
            pos_change = SPEED / 1.41
        # изменение координат
        for direction in pressed_keys:
            if direction == pygame.K_w:
                self.y += pos_change * math.sin(self.view)
                self.x += pos_change * math.cos(self.view)
            elif direction == pygame.K_a:
                self.x += pos_change * math.sin(self.view)
                self.y -= pos_change * math.cos(self.view)
            elif direction == pygame.K_s:
                self.x -= pos_change * math.cos(self.view)
                self.y -= pos_change * math.sin(self.view)
            elif direction == pygame.K_d:
                self.x -= pos_change * math.sin(self.view)
                self.y += pos_change * math.cos(self.view)
            # временный поворот камеры
            elif direction == pygame.K_q:
                self.view -= TurningSpeed
            elif direction == pygame.K_e:
                self.view += TurningSpeed