from settings import *
from itertools import islice


class Player:
    def __init__(self):
        self.x, self.y = start_player_pos
        self.view = player_view

    def pos(self):
        return self.x, self.y

    def check_press(self):
        self.MOVE_BUTTONS_PRESS = dict(islice(BUTTONS_PRESS.items(), 4))
        self.TURN_BUTTONS_PRESS = dict(islice(BUTTONS_PRESS.items(), 4, 6))

    def move(self):
        pressed_keys = [key for key, keydown_bool in self.MOVE_BUTTONS_PRESS.items() if
                        keydown_bool]  # зажатые клавиши движения
        full_speed = len(pressed_keys) != 2  # чтобы игрок наискось не двигался в 2 раза быстрее
        if full_speed:
            pos_change = MOVE_SPEED
        else:
            pos_change = MOVE_SPEED / 1.41
        [pressed_keys.append(key) for key, keydown_bool in self.TURN_BUTTONS_PRESS.items() if
         keydown_bool]  # добавление зажатых клавиш поворота
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