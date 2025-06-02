import pygame as pg
import pygame_gui as gui
import sys
import time
from shapely import *

from robot import *
from map import *
from scenes import *
from add_func import *
from Astar import *
from gui_elements import *



def interface():
    global robot, map, walls, tabels, objects, union_objects, param, perception_type, start, target, path, draw_robot, position, inspected_surface, tick

    def define():
        global robot, map, walls, tabels, objects, union_objects, param, perception_type, start, target, path, draw_robot, position, inspected_surface, tick
        objects = np.hstack([walls, tabels])
        union_objects = union_all(objects)
        map = Map(walls,tabels,param["scale"])
        start = (int(param["start"][1]/(param["scale"]/2)),int(param["start"][0]/(param["scale"]/2)))
        target = (int(param["target"][1]/(param["scale"]/2)),int(param["target"][0]/(param["scale"]/2)))
        path = path2real(A_star(map.disc_map, start, target), param["scale"])
        inspected_surface.fill((0,0,0))
        map_obs_surface.fill((255,255,255))
        map.draw_obs(screen, map_obs_surface)
        tick = 0

    sz = (1900, 1000)
    pg.display.set_caption('Sim')
    screen = pg.display.set_mode(sz)

    graph_interface = GUI(sz)

    map_dot_surface = pg.Surface((320, 200))
    map_dot_surface.fill(pg.Color(255,255,255))

    map_disc_surface = pg.Surface((320, 200))
    map_disc_surface.fill(pg.Color(255,255,255))

    map_obs_surface = pg.Surface((1600, 1000))
    map_obs_surface.fill(pg.Color(255,255,255))

    inspected_surface = pg.Surface((1600,1000))

    timer = pg.time.Clock()
    fps = 30
    dt = 1 / fps

    walls, tabels = scenes[0]
    param = params[0]
    perception_type = 0

    define()
    
    robot = Robot(param["start"][0], param["start"][1], param["start"][2], param["scale"])
    speed = 0.5
    draw_robot = False
    
    position = 0

    global_angle = 0
    view_speed = 0.5
    frequency = 30
    f_ind_color = (0,255,0)
    s_ind_color = (0,255,0)
    r_ind_color = (0,255,0)

    while True:
        t = time.time()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit(0)

            if ev.type == gui.UI_BUTTON_PRESSED:
                if ev.ui_element == graph_interface.start_button:
                    define()
                    map_dot_surface.fill(pg.Color(255,255,255))
                    map_disc_surface.fill(pg.Color(255,255,255))
                    robot = Robot(param["start"][0], param["start"][1], param["start"][2], param["scale"])
                    position = 0
                    draw_robot = True

            if ev.type == gui.UI_DROP_DOWN_MENU_CHANGED:
                if ev.ui_element == graph_interface.scene_menu:
                    param = params[int(ev.text)]
                    walls, tabels = scenes[int(ev.text)]
                    define()
                    
                if ev.ui_element == graph_interface.perception_menu:
                    perception_type = PERCEPTION[ev.text]

            if ev.type == gui.UI_TEXT_ENTRY_FINISHED:
                if ev.ui_element == graph_interface.frequency_box:
                    frequency = float(ev.text)
                    f_ind_color = (0,255,0)

                if ev.ui_element == graph_interface.speed_box:
                    speed = float(ev.text)
                    s_ind_color = (0,255,0)

                if ev.ui_element == graph_interface.rotation_speed_box:
                    view_speed = float(ev.text)
                    r_ind_color = (0,255,0)

            if ev.type == gui.UI_TEXT_ENTRY_CHANGED:
                if ev.ui_element == graph_interface.frequency_box:
                    f_ind_color = (255,0,0)

                if ev.ui_element == graph_interface.speed_box:
                    s_ind_color = (255,0,0)

                if ev.ui_element == graph_interface.rotation_speed_box:
                    r_ind_color = (255,0,0)
                    
            graph_interface.manager.process_events(ev)
        
        screen.fill((255, 255, 255))
        pg.draw.polygon(screen, (0,0,0), ((1600,0), (1900,0), (1900,500), (1600,500)))
        pg.draw.circle(screen, f_ind_color, graph_interface.frequency_ind, 5)
        pg.draw.circle(screen, s_ind_color, graph_interface.speed_ind, 5)
        pg.draw.circle(screen, r_ind_color, graph_interface.rotation_ind, 5)
        
        try:
            pg.draw.polygon(inspected_surface, (220, 255, 200), robot.poly.exterior.coords)
            inspected_surface.set_colorkey((0,0,0))  
            screen.blit(inspected_surface, (0,0))
        except:
            pass

        screen.blit(map_obs_surface)
        for point in path:
            if path.index(point) == 0:
                drawText(screen, "S", point[0], point[1])
            if path.index(point) == len(path)-1:
                drawText(screen, "G", point[0], point[1])
            pg.draw.circle(screen, (0, 0, 255), point, 3)

        if draw_robot:
            robot.draw(screen)
            robot.goto(path[position], objects, dt, speed)
            if euclidean_distance(robot.getPos(), path[position]) < 20 and position < len(path)-1:
                position+=1
            robot.view_control(screen,perception_type,union_objects,dt,global_angle,view_speed,tick%int(fps/frequency)==0)
        
        if euclidean_distance(robot.getPos(), param["target"]) < 30:
            space = Polygon([(0,0),(0,1000),(1600,1000),(1600,0)])
            space = intersection(space, LineString(path).buffer(param["scale"]*8))
            for o in objects:
                space = space.difference(o)
            result = robot.inspected_poligon.area/space.area
            draw_robot = False
            graph_interface.result_label.set_text(f"{round(result*100,0)}%")

        map.draw_dot(screen, map_dot_surface, robot)
        map.draw_disc(screen, map_disc_surface)

        tick+=1

        graph_interface.manager.update(dt)
        graph_interface.manager.draw_ui(screen)

        pg.display.flip()
        timer.tick(1/dt)


if __name__ == "__main__":
    interface()
