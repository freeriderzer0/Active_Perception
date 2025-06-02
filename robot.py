import numpy as np
import pygame as pg
from shapely import *
from math import *
from add_func import *
import time

class Robot:
    def __init__(self, x, y, alpha, scale):

        self.x, self.y, self.alpha, self.scale = x, y, alpha, scale

        self.view_angle = self.alpha
        self.speed = 0

        self.analit_angle = radians(320)
        self.num_rays_in_aa = 160

        self.fov = radians(80)
        self.num_rays_in_fov = 80

        self.ray_len = 8*self.scale

        self.squares = []
        self.counters = []
        
        self.views = [radians(-120),radians(-80),radians(-40),radians(0),radians(40),radians(80),radians(120)]
        self.inspected_poligon = Point(self.x,self.y).buffer(1)

        self.map_dots = []
        self.dots = []

        self.poly = None

        self.v = 0
        self.tar_v = 0

    def getPos(self):
        return [self.x, self.y]

    def draw(self, screen):
        pg.draw.circle(screen, (0,0,255), (self.x, self.y), 0.25*self.scale)
        pg.draw.line(screen, (0,0,255), (self.x, self.y), (self.x + cos(self.alpha)*30, self.y + sin(self.alpha)*30), 4)

    def move(self, objects, delta):
        key = pg.key.get_pressed()
        key2 = pg.key.get_pressed()
        cos_a, sin_a = cos(self.alpha), sin(self.alpha)

        if key2[pg.K_LSHIFT]:
            self.speed += 5
            if self.speed >= 1*self.scale:
                self.speed = 1*self.scale
        else:
            self.speed = 0.5*self.scale

        dx, dy = 0, 0
        if key[pg.K_w]:
            dx = cos_a * delta * self.speed
            dy = sin_a * delta * self.speed
        if key[pg.K_s]:
            dx = cos_a * delta * -self.speed
            dy = sin_a * delta * -self.speed
        if key[pg.K_a]:
            dx = sin_a * delta * self.speed
            dy = cos_a * delta * -self.speed
        if key[pg.K_d]:
            dx = sin_a * delta * -self.speed
            dy = cos_a * delta * self.speed
        if key[pg.K_RIGHT]:
            self.alpha += 0.5 * delta
        if key[pg.K_LEFT]:
            self.alpha -= 0.5 * delta

        if any(Point(self.x + dx, self.y + dy).buffer(0.25*self.scale).intersects(objects)):
            dx, dy = 0, 0
        self.x += dx
        self.y += dy

    def raycast(self, angle, num_rays, ray_len, alpha, objects):
        dots = []
        dots_mask = []
        for i in range(num_rays):
            line = LineString(((self.x, self.y), (self.x + cos(alpha - angle/2 + i * angle/num_rays) * ray_len, self.y + sin(alpha - angle/2 + i * angle/num_rays) * ray_len)))
            intersection = line.intersection(objects)
            try:
                try:
                    dot = intersection.coords[0]
                except:
                    dot = intersection.geoms[0].coords[0]
                mask = True
            except:
                dot = (self.x + cos(alpha - angle/2 + i * angle/num_rays) * ray_len, self.y + sin(alpha - angle/2 + i * angle/num_rays) * ray_len)
                mask = False
            dots.append(dot)
            dots_mask.append(mask)
        return dots, dots_mask

    def analit(self, objects, screen, global_angle):
        dots, mask = self.raycast(self.analit_angle, self.num_rays_in_aa, self.ray_len, self.alpha, objects)
        for dot in dots:
            pg.draw.circle(screen, (255, 0, 0), dot, 2)
            if dots.index(dot) == 0 or dots.index(dot) == self.num_rays_in_aa - 1:
                pg.draw.line(screen, (255, 0, 0), (self.x, self.y), dot, 2)

        self.squares = []
        self.counters = []

        for i in range(7):
            dotsd_square = dots[i*20:i*20+40]
            dotsd_square.append((self.x, self.y))
            dots_counter = mask[i*20:i*20+40]
            self.squares.append((Polygon(dotsd_square).difference(self.inspected_poligon)).area)
            self.counters.append(sum(dots_counter))

        if global_angle == 1:
            try:
                self.tar_v = self.alpha + self.views[self.squares.index(max(self.squares))]
            except:
                self.tar_v = self.alpha + self.views[3]
            
       
    def view_control(self,screen,perception_type,objects,delta, global_angle, view_speed, flag):
        if perception_type == 0:
            self.view_angle = self.alpha
        if perception_type == 1:
            if flag: self.analit(objects, screen, global_angle)
            if global_angle == 0:
                try:
                    self.tar_v = self.alpha + self.views[self.squares.index(max(self.squares))]
                except:
                    self.tar_v = self.alpha + self.views[3]
            if abs(self.tar_v-self.view_angle) > 0.013:
                self.view_angle += (self.tar_v-self.view_angle)/abs(self.tar_v-self.view_angle) * view_speed * delta
        if perception_type == 2:
            self.v += view_speed * delta
            self.view_angle = self.alpha + self.v

        dots, mask = self.raycast(self.fov, self.num_rays_in_fov, self.ray_len, self.view_angle, objects)
        self.dots = np.array(dots)[mask]

        self.map_dots.extend(np.array(dots)[mask])

        for dot in dots:
            pg.draw.circle(screen, (26, 115, 3), dot, 2)
            if dots.index(dot) == 0 or dots.index(dot) == self.num_rays_in_fov - 1:
                pg.draw.line(screen, (26, 115, 3), (self.x, self.y), dot, 2)
        pol_dots = dots
        pol_dots.append((self.x, self.y))
        self.poly = Polygon(pol_dots)
        self.inspected_poligon = union(self.inspected_poligon,self.poly.difference(self.inspected_poligon))

    def goto(self, target, objects, dt, speed):
        self.speed = speed*self.scale
        vector2target = np.subtract(target, self.getPos())
        angle2target = math.atan2(vector2target[1], vector2target[0])
        d_angle = limAng(angle2target - self.alpha)
        # d_angle = angle2target - self.alpha
        self.alpha += d_angle*dt
        # self.alpha += d_angle
        cos_a, sin_a = cos(self.alpha), sin(self.alpha)
        dx = cos_a * dt * self.speed
        dy = sin_a * dt * self.speed
        if any(Point(self.x + dx, self.y + dy).buffer(0.25*self.scale).intersects(objects)):
            dx, dy = 0, 0
        self.x += dx
        self.y += dy
