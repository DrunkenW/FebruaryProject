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
        for wall in walls:  # Используем walls вместо map
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

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
