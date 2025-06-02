import numpy as np
import pygame as pg
import cv2
from shapely import *
from math import *
from add_func import *
import matplotlib.pyplot as plt

class Map:
    def __init__(self, walls, tabels, scale):
        self.odstacles = np.hstack([walls, tabels])
        self.walls = walls
        self.tabels = tabels
        self.scale = scale/2

        self.discretes = []
        self.disc_map = np.zeros((int(1000/self.scale),int(1600/self.scale)),np.uint8)
        for h in range(int(1000/self.scale)):
            for w in range(int(1600/self.scale)):
                x0, y0 = w*self.scale+1,h*self.scale+1
                p = Polygon([(x0, y0),(x0+self.scale-2,y0),(x0+self.scale-2,y0+self.scale-2),(x0,y0+self.scale-2)])
                if any(p.intersects(self.odstacles)):
                    self.disc_map[h][w] = 1
                    continue
                self.discretes.append(p)
        self.discretes = np.array(self.discretes, dtype=object)
        # print(self.discretes)
        # print(self.disc_map)


    def draw_obs(self, screen, surface):
        for o in self.tabels:
            coor = list(o.exterior.coords)
            for interior in o.interiors:
                coor+=interior.coords[:]
            pg.draw.polygon(surface, (100,100,100), coor)
        for o in self.walls:
            coor = list(o.exterior.coords)
            for interior in o.interiors:
                coor+=interior.coords[:]
            pg.draw.polygon(surface, (0,0,0), coor)
        surface.set_colorkey((255,255,255))  
        screen.blit(surface, (0,0))
        

    def draw_dot(self, screen, surface,robot):
        # surface.fill(pg.Color(255,255,255))
        for dot in robot.dots:
            pg.draw.circle(surface, (255, 0, 0), (dot[0]/5,dot[1]/5), 1)
        screen.blit(surface, (1565,50))

        # dots = np.array(robot.map_dots)/5
        # dotx = []
        # doty = []
        # for dot in dots:
        #     dotx.append(dot[0])
        #     doty.append(dot[1])
        # # cv2.imshow("Discrere Map", dots)
        # # cv2.waitKey(1)

        # plt.scatter(dotx,doty)
        # plt.show()

    def draw_disc(self, screen, surface):
        surface.fill(pg.Color(255,255,255))
        # # for disc in self.discretes:
        # #     coor = np.array(disc.exterior.coords)
        # #     pg.draw.polygon(surface, (150,150,150), coor/5)
        # # screen.blit(surface, (1565,230))

        img = cv2.bitwise_not(cv2.resize(self.disc_map*255, (320,200), interpolation=cv2.INTER_NEAREST))
        cv2.imwrite('resources/map.png', img)
        # cv2.imshow("Discrere Map", img)
        # cv2.waitKey(1)
        screen.blit(pg.image.load('resources/map.png'), (1565,275))
