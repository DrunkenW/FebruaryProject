from settings import *


class WorldMap:
    def __init__(self):
        self.text_map = [
            "WWWWWWWWWWWW",
            "W          W",
            "W          W",
            "W          W",
            "W          W",
            "W          W",
            "W          W",
            "WWWWWWWWWWWW"
        ]
        self.WORLD_MAP = set()
        self.WALL_SIZE = WALL_SIZE

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
            pygame.draw.rect(sc, DARK_GRAY, wall_rect, 1)
