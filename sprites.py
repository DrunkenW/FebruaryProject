import pygame
from settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'barrel': {
                'sprite': pygame.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
            },
            'devil': {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True, # углы обзора спрайта
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,},
        }



        self.list_of_objects = [
            # Монстры (5 шт) - стратегические точки
            SpriteObject(self.sprite_parameters['devil'],  (4.5, 3.5)),
            SpriteObject(self.sprite_parameters['devil'], (16.5, 6.5)),
            SpriteObject(self.sprite_parameters['devil'], (10.5, 12.5)),
            SpriteObject(self.sprite_parameters['devil'], (22.5, 9.5)),
            SpriteObject(self.sprite_parameters['devil'], (7.5, 15.5)),

            # Факелы x2 (60 шт) - вдоль стен с отступом 0.1
            # Бочки x2 (30 шт) - углы и тупики
            SpriteObject(self.sprite_parameters['barrel'], (2 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (5 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (9 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (14 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (19 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (23 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (4 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (11 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (17 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (21 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (6 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (13 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (18 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (24 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (3 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (8 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (15 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (22 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (5 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (12 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (20 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (7 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (14 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (19 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (2 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (10 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (17 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (23 + 0.9, 13 + 0.9)),
        ]
        """
            *[SpriteObject(self.sprite_parameters['torch'], True, (x + 0.1, y + 0.1), 1.6, 0.4)
              for x in range(1, 27, 3) for y in [1, 6, 9, 13]],  # Основные линии
            *[SpriteObject(self.sprite_parameters['torch'], True, (x + 0.1, y + 0.1), 1.6, 0.4)
              for x, y in [(3, 2), (8, 4), (14, 7), (19, 5), (24, 10), (10, 12), (17, 14)]],  # Дополнительные
            """

class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

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
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEF / distance_to_sprite * self.scale), HEIGHT * 2)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (current_ray * SCALE - half_proj_height, HEIGHT // 2 - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)