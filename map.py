from settings import *

text_map = [
    '111111111111',
    '1......1...1',
    '1..111...1.1',
    '1....1..11.1',
    '1..2....1..1',
    '1..2...111.1',
    '1....1.....1',
    '1111111111111'
]

world_map = {}
walls = []

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            wall_pos = (i * WALL_SIZE, j * WALL_SIZE)
            walls.append(pygame.Rect(wall_pos[0], wall_pos[1], WALL_SIZE, WALL_SIZE))
            if char == '1':
                world_map[wall_pos] = '1'
            elif char == '2':
                world_map[wall_pos] = '2'