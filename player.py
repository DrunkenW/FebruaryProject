import pygame.draw

from settings import *
from itertools import islice


class Player:
    def __init__(self):
        self.x, self.y = start_player_pos
        self.player_direction_of_view = player_direction_of_view
        self.drawing_range = DRAWING_RANGE
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

    def vision(self, sc, map):
        cur_angle = self.player_direction_of_view - FOV / 2  # Начальный угол для первого луча
        xo, yo = self.pos()  # Позиция игрока
        for ray in range(RAYS_INT):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            depth = 0
            hit_wall = False
            while depth < DRAWING_RANGE:
                x = xo + depth * cos_a
                y = yo + depth * sin_a
                wall_pos = (int(x // WALL_SIZE) * WALL_SIZE, int(y // WALL_SIZE) * WALL_SIZE)
                if wall_pos in map:
                    hit_wall = True
                    break
                depth += 1

            if hit_wall:
                # Корректировка глубины с учетом угла между лучом и направлением взгляда
                corrected_depth = depth * math.cos(self.player_direction_of_view - cur_angle)
                # Расчет высоты проекции стены
                proj_height = PROJ_COEF / (corrected_depth + 0.0001)
                proj_height = min(proj_height, HEIGHT)  # Ограничение высоты
                # Расчет цвета в зависимости от глубины
                c = 255 / (1 + corrected_depth * corrected_depth * 0.0001)
                color = (c // 2, c, c // 3)
                # Отрисовка вертикальной линии (стены)
                wall_column = pygame.Rect(ray * SCALE, HEIGHT / 2 - proj_height / 2, SCALE, proj_height)
                pygame.draw.rect(sc, color, wall_column)

            cur_angle += DELTA_ANGLE  # Переход к следующему лучу
