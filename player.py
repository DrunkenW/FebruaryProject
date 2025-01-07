import pygame
import math
from settings import *

class Player:
    def __init__(self):
        self.x, self.y = start_player_pos  # Начальная позиция игрока
        self.angle = player_angle  # Угол направления взгляда
        self.speed = player_speed  # Скорость движения игрока
        self.rotation_speed = TurningSpeed  # Скорость поворота

    @property
    def pos(self):
        return self.x, self.y

    def movement(self, map):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y

        # Движение вперед и назад
        if keys[pygame.K_w]:  # Вперед
            new_x += math.cos(self.angle) * self.speed
            new_y += math.sin(self.angle) * self.speed
        if keys[pygame.K_s]:  # Назад
            new_x -= math.cos(self.angle) * self.speed
            new_y -= math.sin(self.angle) * self.speed

        # Движение влево и вправо (страф)
        if keys[pygame.K_a]:  # Влево
            new_x += math.cos(self.angle - math.pi / 2) * self.speed
            new_y += math.sin(self.angle - math.pi / 2) * self.speed
        if keys[pygame.K_d]:  # Вправо
            new_x += math.cos(self.angle + math.pi / 2) * self.speed
            new_y += math.sin(self.angle + math.pi / 2) * self.speed

        # Проверка коллизий
        collision = False
        for wall in map:
            wall_rect = pygame.Rect((wall[0], wall[1], WALL_SIZE, WALL_SIZE))
            if wall_rect.collidepoint(new_x, new_y):
                collision = True
                break

        if not collision:
            self.x, self.y = new_x, new_y

        # Поворот
        if keys[pygame.K_LEFT]:  # Поворот влево
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:  # Поворот вправо
            self.angle += self.rotation_speed

        # Нормализация угла
        self.angle %= 2 * math.pi

    def ray_casting(self, sc, world_map):
        ox, oy = self.pos
        mapping = lambda a, b: ((a // 100) * 100, (b // 100) * 100)
        xm, ym = mapping(ox, oy)
        cur_angle = self.angle - FOV / 2
        SCALE = WIDTH / RAYS_INT
        for ray in range(RAYS_INT):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # Поиск пересечения с вертикальными линиями
            x, dx = (xm + 100, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, WIDTH, 100):
                depth_v = (x - ox) / cos_a
                y = oy + depth_v * sin_a
                if mapping(x + dx, y) in world_map:
                    break
                x += dx * 100

            # Поиск пересечения с горизонтальными линиями
            y, dy = (ym + 100, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, HEIGHT, 100):
                depth_h = (y - oy) / sin_a
                x = ox + depth_h * cos_a
                if mapping(x, y + dy) in world_map:
                    break
                y += dy * 100

            # Выбор минимальной глубины
            depth = depth_v if depth_v < depth_h else depth_h
            depth *= math.cos(self.angle - cur_angle)  # Коррекция глубины

            # Расчёт высоты проекции и цвета
            proj_height = PROJ_COEF / depth
            c = 255 / (1 + depth * depth * 0.00002)
            color = (c, c // 2, c // 3)

            # Отрисовка стен
            pygame.draw.rect(sc, color, (int(ray * SCALE), int(HEIGHT / 2 - proj_height / 2), int(SCALE + 2), int(proj_height)))

            # Переход к следующему лучу
            cur_angle += DELTA_ANGLE