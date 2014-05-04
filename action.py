#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sprite import *
from engine import WIDTH, HEIGHT, velocidad, Max_Number_Conversation
from interfaz import *


class Action:
    def __init__(self, screen,cursor, mouvement, MapTest):
        self.current_action = None
        self.screen = screen
        self.cursor = cursor
        self.mouvement = mouvement
        self.MapTest = MapTest

    def iteration_jump(self,sens, MapTest, screen, mouvement , time,stop, demo,perso):
        pygame.time.Clock().tick(10)
        perso.rect.move_ip(0,sens)
        screen.fill((0,0,0))
        MapTest.update(screen, mouvement, False, False, False)
        MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=None,perso_demo=None)
        screen.blit(MapTest.OverMap.imagen, MapTest.mapa.rect)
        pygame.display.update()

    def jump(self, MapTest, screen, mouvement , time,stop, demo,perso):
        self.iteration_jump(-20,MapTest, screen, mouvement , time,stop, demo,perso)
        self.iteration_jump(20,MapTest, screen, mouvement , time,stop, demo,perso)
        self.iteration_jump(-20,MapTest, screen, mouvement , time,stop, demo,perso)
        self.iteration_jump(20,MapTest, screen, mouvement , time,stop, demo,perso)

    def Talk(self, perso_colision, time):
        list_dialogues=perso_colision.get_list_dialogues()
        for key in xrange(Max_Number_Conversation):
            if key in list_dialogues:
                parm_dialogue = list_dialogues[key]
                self.stop_move = True
                if parm_dialogue[0] == 'None':
                    self.draw_dialog_window(perso_colision.get_name() + ": "+ parm_dialogue[1].strip(), perso_colision,time)
                else:
                    repitition = int(parm_dialogue[0])
                    if repitition > 1:
                        parm_dialogue[0] = repitition -1
                        self.draw_dialog_window(perso_colision.get_name() + ": "+ parm_dialogue[1].strip(), perso_colision,time)
                    else:
                        parm_dialogue = list_dialogues.pop(key)
                        self.draw_dialog_window(perso_colision.get_name() + ": "+ parm_dialogue[1].strip(), perso_colision,time)
                self.stop_move = False
                break
    def draw_dialog_window(self, text, perso_colision, time):
        bag_image_desc_bar = Image('graphics/bar1.png')
        bag_image_desc_bar.change_size(WIDTH, HEIGHT*0.09)
        text_info_name = Text(text=(text), left=bag_image_desc_bar.rect.left+20, top = bag_image_desc_bar.rect.top+10)
        BagWindow_desc = Window(width=bag_image_desc_bar.rect.w, height=bag_image_desc_bar.rect.h, left=0, top=0.8*HEIGHT, moveable=False)
        BagWindow_desc.appendText(text_info_name)
        BagWindow_desc.appendBGImage(bag_image_desc_bar)
        BagWindow_desc.update(self.screen, self.cursor)
        menu_ON = True
        while menu_ON:
            self.MapTest.update(self.screen, self.mouvement, None, True)
            self.screen.blit(self.MapTest.OverMap.imagen, self.MapTest.mapa.rect)
            self.MapTest.MobsUpdate(self.screen, self.mouvement, time, True, True,stop=True, demo=True,perso_demo=None)
            BagWindow_desc.update(self.screen, self.cursor)
            self.cursor.update()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu_ON = False
