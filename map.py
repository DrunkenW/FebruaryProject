from settings import *


class Map:
    def __init__(self):
        self.text_map = [
            'WWWWWWWWWWWW',
            'W......W...W',
            'W..WWW...W.W',
            'W....W..WW.W',
            'W..W....W..W',
            'W..W...WWW.W',
            'W....W.....W',
            'WWWWWWWWWWWW'
        ]

        self.world_map = set()
        self.mini_map = set()
        self.WALL_SIZE = WALL_SIZE
        self.create_map() # заполнение self.world_map объектами

    def create_map(self):
        for j, row in enumerate(self.text_map):
            for i, obj in enumerate(row):
                if obj == "W":
                    self.world_map.add((i * self.WALL_SIZE, j * self.WALL_SIZE))
                    self.mini_map.add((i * 20, j * 20))

    def draw_map(self, sc):
        # отрисовка стен
        for wall in self.world_map:
            x, y = wall
            wall_rect = pygame.Rect(x, y, self.WALL_SIZE, self.WALL_SIZE)
            pygame.draw.rect(sc, DARKGRAY, wall_rect, 1)

    def get_map(self):
        return self.world_map

    def get_minimap(self):
        return self.mini_map
