import pygame as pg
import pygame_gui as gui
import sys
import time
from shapely import *
import os.path
import sys
import json

from robot import *
from map import *
from scenes import *
from add_func import *
from Astar import *
from gui_elements import *



def interface(hz, ga, active, speed, view_speed):
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
    perception_type = active

    define()
    
    robot = Robot(param["start"][0], param["start"][1], param["start"][2], param["scale"])
    draw_robot = True
    
    position = 0

    frequency = hz
    global_angle = ga

    ind_color = (0,255,0)

    while True:
        t = time.time()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit(0)

            if ev.type == gui.UI_BUTTON_PRESSED:
                if ev.ui_element == graph_interface.start_button:
                    define()
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
                    ind_color = (0,255,0)

            if ev.type == gui.UI_TEXT_ENTRY_CHANGED:
                if ev.ui_element == graph_interface.frequency_box:
                    ind_color = (255,0,0)
                    
            graph_interface.manager.process_events(ev)
        
        screen.fill((255, 255, 255))
        pg.draw.polygon(screen, (0,0,0), ((1600,0), (1900,0), (1900,500), (1600,500)))
        pg.draw.circle(screen, ind_color, graph_interface.frequency_ind, 5)
        
        try:
            pg.draw.polygon(inspected_surface, (182, 245, 137), robot.poly.exterior.coords)
            inspected_surface.set_colorkey((0,0,0))  
            screen.blit(inspected_surface, (0,0))
        except:
            pass

        screen.blit(map_obs_surface)
        # map.draw_obs(screen)
        for point in path:
            pg.draw.circle(screen, (255, 0, 0), point, 3)

        if draw_robot:
            robot.draw(screen)
            # robot.move(objects, dt)
            try:
                robot.goto(path[position], objects, dt, speed)
            except:
                space = Polygon([(0,0),(0,1000),(1600,1000),(1600,0)])
                space = intersection(space, LineString(path).buffer(param["scale"]*8))
                for o in objects:
                    space = space.difference(o)
                result = robot.inspected_poligon.area/space.area
                draw_robot = False
                graph_interface.result_label.set_text(f"{round(result*100,0)}%")
                return result
            if euclidean_distance(robot.getPos(), path[position]) < 20:
                position+=1
            if tick%int(fps/frequency) == 0:
                robot.analit(union_objects, screen, global_angle)
            robot.view_control(screen,perception_type,union_objects,dt,global_angle,view_speed)
        
        if euclidean_distance(robot.getPos(), param["target"]) < 30:
            space = Polygon([(0,0),(0,1000),(1600,1000),(1600,0)])
            space = intersection(space, LineString(path).buffer(param["scale"]*8))
            for o in objects:
                space = space.difference(o)
            result = robot.inspected_poligon.area/space.area
            draw_robot = False
            graph_interface.result_label.set_text(f"{round(result*100,0)}%")
            return result

        tick+=1

        # map.draw_dot(screen, map_dot, robot)
        # map.draw_disc(screen, map_disc)

        graph_interface.manager.update(dt)
        graph_interface.manager.draw_ui(screen)

        drawText(screen, f"Coords = {int(robot.x), int(robot.y)}", 5, 1)
        # dt = (time.time()-t)
        drawText(screen, f"FPS = {int(1/dt)}", 5, 23)

        pg.display.flip()
        timer.tick(1/dt)


if __name__ == "__main__":
    results = {}
    hz = 3
    glob = 0
    speed = 0.5
    for active in [1,2]:
        results[f"{active}"] = []
        for view_speed in np.arange(0.2, 1.2, 0.2):
            result = interface(hz,glob,active,speed,view_speed)
            # with open("results.txt", "a") as file:
                # file.write(f'{hz} / {glob}: {result}\n')
            results[f"{active}"].append((view_speed,result))
    with open("results/results_view_speed.json", "w") as fh:
        json.dump(results, fh) 