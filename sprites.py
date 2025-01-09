from settings import *

class Sprites:
    def __init__(self):
        self.sprite_types = {
            'devil': [pygame.image.load(f'sprites/devil/0.png').convert_alpha()]
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['devil'], False, (7, 4), -0.2, 0.7),
        ]

class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * SPRITE_SIZE, pos[1] * SPRITE_SIZE
        self.shift = shift
        self.scale = scale