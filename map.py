from settings import *

text_map = [
    'WWWWWWWWWWWW',
    'W......W...W',
    'W..WWW...W.W',
    'W....W..WW.W',
    'W..W....W..W',
    'W..W...WWW.W',
    'W....W.....W',
    'WWWWWWWWWWWW'
]

world_map = set()
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * WALL_SIZE, j * WALL_SIZE))
            mini_map.add((i * 20, j * 20))

    def create_map(self):
        for j, row in enumerate(self.text_map):
            for i, obj in enumerate(row):
                if obj == "W":
                    self.WORLD_MAP.add((i * self.WALL_SIZE, j * self.WALL_SIZE))

    def draw_map(self, sc):
        # отрисовка стен
        for wall in self.WORLD_MAP:
            x, y = wall
            wall_rect = pygame.Rect(x, y, self.WALL_SIZE, self.WALL_SIZE)
            pygame.draw.rect(sc, DARKGRAY, wall_rect, 1)

    def get_map(self):
        return self.WORLD_MAP