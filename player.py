from settings import *
from itertools import islice


class Player:
    def __init__(self):
        self.x, self.y = start_player_pos
        self.player_direction_of_view = player_direction_of_view

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
                self.y += pos_change * math.sin(self.player_direction_of_view)
                self.x += pos_change * math.cos(self.player_direction_of_view)
            elif direction == pygame.K_a:
                self.x += pos_change * math.sin(self.player_direction_of_view)
                self.y -= pos_change * math.cos(self.player_direction_of_view)
            elif direction == pygame.K_s:
                self.x -= pos_change * math.cos(self.player_direction_of_view)
                self.y -= pos_change * math.sin(self.player_direction_of_view)
            elif direction == pygame.K_d:
                self.x -= pos_change * math.sin(self.player_direction_of_view)
                self.y += pos_change * math.cos(self.player_direction_of_view)
            # временный поворот камеры
            elif direction == pygame.K_q:
                self.player_direction_of_view -= TurningSpeed
            elif direction == pygame.K_e:
                self.player_direction_of_view += TurningSpeed

    def vision(self, sc):
        # отрисовка лучей обзора
        player_pos = self.pos()
        xo, yo = player_pos
        angle = self.player_direction_of_view - FOV / 2
        for ray in range(RAYS_INT):
            sina = math.sin(angle)
            cosa = math.cos(angle)
            x = xo + DRAWING_RANGE * cosa
            y = yo + DRAWING_RANGE * sina
            pygame.draw.line(sc, (255, 255, 255), player_pos, (x, y))
            angle += DELTA_ANGEL  # изменение угла
