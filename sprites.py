import pygame
from settings import *


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'devil': [pygame.image.load(f'sprites/devil/{i}.png').convert_alpha() for i in range(8)],
            'torch': pygame.image.load("sprites/torch/0 (1).png"),
            'barrel': pygame.image.load("sprites/barrel/0.png"),
            'scream_torch': pygame.image.load("sprites/torch/1.png"),
            'scream': pygame.image.load("sprites/scream/0.png")
        }
        self.list_of_objects = [
            # Монстры (5 шт) - стратегические точки
            SpriteObject(self.sprite_types['devil'], False, (4.5, 3.5), -0.2, 0.7),
            SpriteObject(self.sprite_types['devil'], False, (16.5, 6.5), -0.2, 0.7),
            SpriteObject(self.sprite_types['devil'], False, (10.5, 12.5), -0.2, 0.7),
            SpriteObject(self.sprite_types['devil'], False, (22.5, 9.5), -0.2, 0.7),
            SpriteObject(self.sprite_types['devil'], False, (7.5, 15.5), -0.2, 0.7),

            # Факелы x2 (60 шт) - вдоль стен с отступом 0.1
            *[SpriteObject(self.sprite_types['torch'], True, (x + 0.1, y + 0.1), 1.6, 0.4)
              for x in range(1, 27, 3) for y in [1, 6, 9, 13]],  # Основные линии
            *[SpriteObject(self.sprite_types['torch'], True, (x + 0.1, y + 0.1), 1.6, 0.4)
              for x, y in [(3, 2), (8, 4), (14, 7), (19, 5), (24, 10), (10, 12), (17, 14)]],  # Дополнительные

            # Бочки x2 (30 шт) - углы и тупики
            *[SpriteObject(self.sprite_types['barrel'], True, (x + 0.9, y + 0.9), 1.8, 0.4)
              for x, y in [(2, 3), (5, 3), (9, 3), (14, 3), (19, 3), (23, 3),
                           (4, 5), (11, 5), (17, 5), (21, 5), (6, 7), (13, 7),
                           (18, 7), (24, 7), (3, 8), (8, 8), (15, 8), (22, 8),
                           (5, 10), (12, 10), (20, 10), (7, 11), (14, 11), (19, 11),
                           (2, 13), (10, 13), (17, 13), (23, 13)]]
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * WALL_SIZE, pos[1] * WALL_SIZE
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= RAYS_INT - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            proj_height = min(int(PROJ_COEF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height, HEIGHT // 2 - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)