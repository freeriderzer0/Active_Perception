import math
import pygame as pg

pg.font.init()
font = pg.font.SysFont('freesansbold', 24)

PERCEPTION = {"Active":1, "Standard":0, "Rotation":2}

def drawText(screen, s, x, y):
    surf = font.render(s, True, (0, 0, 255))
    screen.blit(surf, (x, y))

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def limAng(ang):
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def path2real(path, scale):
    real_path = []
    for point in path:
        real_path.append((point[1]*(scale/2)+(scale/4),point[0]*(scale/2)+(scale/4)))
    return real_path