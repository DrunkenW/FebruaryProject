from settings import *

# отрисовка лучей обзора
def view(sc, player_pos, player_view):
    xo, yo = player_pos
    angle = player_view - FOV / 2
    for ray in range(RAYS_INT):
        sina = math.sin(angle)
        cosa = math.cos(angle)
        x = xo + DRAWING_RANGE * cosa
        y = yo + DRAWING_RANGE * sina
        pygame.draw.line(sc, (255, 255, 255), player_pos, (x, y))
        angle += DELTA_ANGEL # изменение угла