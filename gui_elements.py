import pygame_gui as gui
import pygame as pg
from scenes import *

class GUI:
    def __init__(self,sz):    
        self.manager = gui.UIManager(sz)
        self.manager.get_theme().load_theme('resources/theme.json')

        self.scene_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,500), (100, 50)),
                                                    text="Scene:",
                                                    manager=self.manager)

        self.scene_menu = gui.elements.UIDropDownMenu(relative_rect=pg.Rect((1700,500), (100, 50)),
                                                    options_list=[str(i) for i in range(len(scenes))],
                                                    starting_option='0',
                                                    manager=self.manager)
            
        self.perception_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,550), (150, 50)),
                                                    text="Perception:",
                                                    manager=self.manager)
            
        self.perception_menu = gui.elements.UIDropDownMenu(relative_rect=pg.Rect((1750,550), (100, 50)),
                                                    options_list=['Standart','Active','Rotation'],
                                                    starting_option='Standart',
                                                    manager=self.manager)
        
        self.frequency_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,600), (150, 50)),
                                                    text="Control Hz:",
                                                    manager=self.manager)
        
        self.frequency_box = gui.elements.UITextEntryLine(relative_rect=pg.Rect((1750,600), (100, 50)),
                                                    initial_text="30",
                                                    manager=self.manager)
        
        self.speed_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,650), (150, 50)),
                                                    text="Speed m/s:",
                                                    manager=self.manager)
        
        self.speed_box = gui.elements.UITextEntryLine(relative_rect=pg.Rect((1750,650), (100, 50)),
                                                    initial_text="0.5",
                                                    manager=self.manager)
        
        self.rotation_speed_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,700), (200, 50)),
                                                    text="Rot.speed rad/s:",
                                                    manager=self.manager)
        
        self.rotation_speed_box = gui.elements.UITextEntryLine(relative_rect=pg.Rect((1800,700), (50, 50)),
                                                    initial_text="0.5",
                                                    manager=self.manager)

        self.start_button = gui.elements.UIButton(relative_rect=pg.Rect((1700,750), (100, 50)),
                                                text='Start',
                                                manager=self.manager)
        
        self.result_name_label = gui.elements.UILabel(relative_rect=pg.Rect((1600,800), (150, 50)),
                                                    text="Inspection:",
                                                    manager=self.manager)
        
        self.result_label = gui.elements.UILabel(relative_rect=pg.Rect((1750,800), (150, 50)),
                                                    text="---%",
                                                    manager=self.manager)
    
        self.frequency_ind = (1860,625)
        self.speed_ind = (1860,675)
        self.rotation_ind = (1860,725)