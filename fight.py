#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine import WIDTH, HEIGHT, velocidad
from sprite import *
from funciones import *
from gui import *
from random import randint
import sys, pygame
import funciones
from chapitre import Chapitre


class Fight:
    # compteur pour associer le personnge l action et le tour
    
    
    def __init__(self, screen,list_player, boss, chapitre):
        
        self.list_player=[]
        self.place=chapitre.get_scene_path()
        self.jugador = list_player
        self.list_ennemi = []
        self.list_monsters = chapitre.get_list_ennemies()
        self.list_action=[]
        self.sound=""
        self.screen = screen
        self.compteur = 0
        self.boss = boss
        self.get_monstre()
        self.status = "menu0"
        self.choix = None
        self.clock = pygame.time.Clock()
        self.cursor = Cursor()
        self.BagWindow = None
        self.init_param_fight_players()
        
    def draw_background(self):
        background_image = load_image(self.place)
        bg_rect = background_image.get_rect()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        self.screen.blit(background_image, bg_rect)    
        
    def draw_player(self):
        i=0
        for player in self.jugador:
            perso_image = load_image(player.fight)
            perso_rect = perso_image.get_rect()
            perso_rect.move_ip(100+150*i,400)
            perso_image = pygame.transform.scale(perso_image, (200, 200))
            self.screen.blit(perso_image, perso_rect)
            i+=1
     
    def init_param_fight_players(self):
        for player in self.jugador:
            player.set_param_fight()
            
    def draw_ennemi(self):
        i=0
        for player in self.list_ennemi:
            perso_image = load_image(player.fight)
            perso_rect = perso_image.get_rect()
            perso_rect.move_ip(100+150*i,300)
            perso_image = pygame.transform.scale(perso_image, (200, 200))
            self.screen.blit(perso_image, perso_rect)
            i+=1
        
    def get_monstre(self):
        if self.boss == True:
            num=1
        else:
            number_monsters = len(self.list_monsters)
            num = funciones.random_number(1, 4)
        for i in range(num):
            monster_index = funciones.random_number(0, number_monsters-1)
            monster_param = self.list_monsters[monster_index]
            ennemi1 = Mounstro(monster_param)
            self.list_ennemi.append(ennemi1)
    
    def get_team_start(self):
        start = funciones.random_number(0, 1)
        if start > 0:
            return self.list_ennemi+self.jugador
        return self.list_player+self.list_ennemi
    
    def draw_main(self):
        self.sequence_fight()

    def gestion_user_event(self, player=None):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.partida_window.collide(self.cursor):
                        self.status = "menu1"
                        click_partida = self.partida_window.collide(1)
                        self.gestion_event(click_partida, player)
                        if click_partida == "Exit":
                            pygame.quit()
                            sys.exit()
                            #pygame.mixer.Sound('sound/Cursor1.wav').play()
                #elif event.button == 3:
                    #pass
            
    def update_screen(self):
        self.cursor.update()
        self.partida_window.update(self.screen, self.cursor)
        pygame.display.update()
    
    def gestion_event(self, case_clicked, player):
        if case_clicked == "Def":
            player.set_def_fight()
            self.choix = "def"
        if case_clicked == "Attack":
            print "Attack"
            attack = ("classic",player.get_attack())
            list_action_player = [player, attack, self.choose_player_to_Attack()]
            self.list_action.append(list_action_player)
            self.choix = "attack"
        if case_clicked == "magie":
            self.open_dialog_window(player)
            print "magie"
            self.choix = "magie"
        if case_clicked == "Objet":
            self.open_bag_window(player)
            self.choix = "objet"
        if case_clicked == "fight":
            self.choix = "fight"
        if case_clicked == "run":
            print "Back"
            pygame.quit()
            sys.exit()
            
                  
    def draw_menu(self):
        pygame.draw.rect(self.screen, (0,0,0), (0,530,800,70), 0)
        image= []
        start_x=12
        start_y=106
        width=24
        heigh=23
        source = 'Graphics/40089.png'
            
        for i in range(3):
            icone = cut_image(source,start_x ,start_y,width ,heigh)
            image.append(pygame.transform.scale(icone, (70, 70)))
            image.append(pygame.transform.scale(icone, (100, 70)))
            start_x += width
            
        (b1, b2, b3) = ('graphics/ground_b1.png', 'graphics/ground_b2.png', 'graphics/ground_b3.png')
        start_b1 = Button(b1, b2, b3, "Fight", text_coord=(280,30),size=14, permanent =False, color=(255,255,255), x=0, y=0, OnClick="fight")
        start_b1.change_image(image[0], image[1], image[0])
        
        start_b2 = Button(b1, b2, b3, "Run away", text_coord=(280,30),size=14, permanent =False, color=(255,255,255), x=70, y=0, OnClick="run")
        start_b2.change_image(image[2], image[3], image[2])
        
        start_b3 = Button(b1, b2, b3, "Status", text_coord=(280,30),size=14, permanent =False, color=(255,255,255), x=140, y=0, OnClick="status")
        start_b3.change_image(image[4], image[5], image[4])
        

        image_text_dest=cut_image(source,85 ,106,66 ,22)
        image.append(pygame.transform.scale(image_text_dest, (205, 70)))
        image_text = Image(source)   
        image_text.ChangeImage(image[6])
        
        self.partida_window = Window(width=200, height=70, left=400, top=530, moveable= False)
        self.partida_window.appendImage(image_text,210)
        self.partida_window.appendButton(start_b1)
        self.partida_window.appendButton(start_b2)
        self.partida_window.appendButton(start_b3)
        
    def draw_menu_second(self, profile):
        image= []
        start_x=12
        start_y=134
        width=24
        heigh=23
        source = 'Graphics/40089.png'
            
        for i in range(6):
            icone = cut_image(source,start_x ,start_y,width ,heigh)
            image.append(pygame.transform.scale(icone, (70, 70)))
            image.append(pygame.transform.scale(icone, (100, 70)))
            start_x += width
            
        (b1, b2, b3) = ('graphics/ground_b1.png', 'graphics/ground_b2.png', 'graphics/ground_b3.png')
        start_b1 = Button(b1, b2, b3, "Attack", text_coord=(660,30),permanent =False,size=14, color=(255,255,255), x=230, y=0, OnClick="Attack")
        start_b1.change_image(image[0], image[1], image[0])
        
        start_b2 = Button(b1, b2, b3, "magie", text_coord=(660,30),size=14, permanent =False,color=(255,255,255), x=300, y=0, OnClick="magie")
        start_b2.change_image(image[2], image[3], image[2])
        
        start_b3 = Button(b1, b2, b3,"Objet", text_coord=(660,30),size=14, permanent =False ,color=(255,255,255), x=370, y=0, OnClick="Objet")
        start_b3.change_image(image[8], image[9], image[8])
        
        start_b4 = Button(b1, b2, b3,"Def", text_coord=(660,30),size=14, permanent =False, color=(255,255,255), x=440, y=0, OnClick="Def")
        start_b4.change_image(image[10], image[11], image[10])
        
        image_text_dest=cut_image(source,85 ,106,66 ,22)
        image.append(pygame.transform.scale(image_text_dest, (310, 70)))
        image_text = Image(source)   
        image_text.ChangeImage(image[12])
        
        image_profile = Image(profile, 0, 0)
        
        self.partida_window = Window(width=800, height=70, left=0, top=530, moveable= False)
        self.partida_window.appendImage(image_profile)
        self.partida_window.appendImage(image_text,510)
        self.partida_window.appendButton(start_b1)
        self.partida_window.appendButton(start_b2)
        self.partida_window.appendButton(start_b3)
        self.partida_window.appendButton(start_b4)
        
    def sequence_fight(self):
        #definir qui va commencer le jeu
            self.list_player=self.get_team_start()
            #if list_player[0] != "Mounstro" and self.status == "menu0":
            while len(self.list_ennemi)>0 and len(self.jugador)>0:
                self.clock.tick(10)
                self.gestion_user_event()
                self.screen.fill((0,100,20))
                self.draw_background()
                self.draw_ennemi()
                self.draw_player()
                self.draw_info_player(self.jugador)
                pygame.draw.rect(self.screen, (0,0,0), (0,530,800,70), 0)
                if self.status == "menu0":
                    self.draw_menu()
                self.update_screen()
                if self.choix == "fight":
                    for player in self.list_player:
                        self.choix = None
                        if player.__class__.__name__ == "Mounstro":
                            list_attack = player.get_list_attack()
                            list_action_player = [player, list_attack[funciones.random_number(0, len(list_attack)-1)],self.jugador[0]]
                            self.list_action.append(list_action_player)             
                        else:
                            while self.choix == None:
                                if self.status != "menu0":
                                    pygame.draw.rect(self.screen, (0,0,0), (0,530,800,70), 0)
                                    self.draw_menu_second(player.getProfile())
                                    self.gestion_user_event(player)
                                    self.update_screen()
                    self.run_sequence()
                    self.check_status()
                    self.status = "menu0"
            print self.list_player
            #self.status = "menu0"
    
    def check_status(self):
        list_to_remove = []
        for player in self.list_player:
            hp = player.get_hp()
            if hp == 0:
                if player.__class__.__name__ == "Mounstro":
                    self.list_ennemi.remove(player)
                    list_to_remove.append(player)
                else:
                    self.jugador.remove(player)
                    list_to_remove.append(player)
        for player in list_to_remove:
            self.list_player.remove(player)
            
    def run_sequence(self):
        for action in self.list_action:
            perso_attaquant = action[0]
            attaque = action[1]
            attaque_value = int(attaque[1])
            pesro_attaque = action[2]
            pesro_attaque.subir_attack(attaque_value - pesro_attaque.get_def_fight())
            
    def draw_info_player(self, jugadors):
        position = 50
        self.BagWindow_desc = Window(width=50, height=150, left=340, top=0, moveable=False)
        
        for player in jugadors:
            bag_image_desc_bar = Image('graphics/bar1.png')
            bag_image_desc_bar.change_size(0.7*bag_image_desc_bar.rect.w, bag_image_desc_bar.rect.h*2)
            bag_image_desc_bar.rect.left = position
            text_info_name = Text(text=str(player.get_name()), left=bag_image_desc_bar.rect.left+20, top = bag_image_desc_bar.rect.top+10) 
            text_info_hp = Text(text="HP: "+str(player.get_hp()), left=bag_image_desc_bar.rect.left+20, top = bag_image_desc_bar.rect.top+30)
            text_info_sp = Text(text="SP: "+str(player.get_sp()), left=bag_image_desc_bar.rect.left+20, top = bag_image_desc_bar.rect.top+50)
            self.BagWindow_desc.appendBGImage(bag_image_desc_bar)
            self.BagWindow_desc.appendText(text_info_name)
            self.BagWindow_desc.appendText(text_info_hp)
            self.BagWindow_desc.appendText(text_info_sp)
            self.BagWindow_desc.update(self.screen, self.cursor)
            position+=100

    
    def gerer_menu_fight(self, click_partida):
        if click_partida == "Attack":
            self.choose_player_to_Attack()
        elif click_partida == "Def":
            print "Def"
        
    def choose_player_to_Attack(self):
        fleche_image = load_image('fleche.png', True, alpha=1)
        i=1

        player_to_attack = None
        modulo = len(self.list_ennemi)
        while player_to_attack==None:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        if i > 1:
                            i-=1
                    if event.key == K_RIGHT:
                        if i < modulo:
                            i+=1
                    if event.key == K_RETURN:
                        player_to_attack = i-1   
            self.screen.fill((0,100,20))
            self.draw_background()
            bg_rect = fleche_image.get_rect()
            bg_rect.move_ip(160*i,290)
            self.draw_ennemi()
            self.draw_player()
            pygame.draw.rect(self.screen, (0,0,0), (0,530,800,70), 0)
            self.screen.blit(fleche_image, bg_rect)
            self.update_screen()
        self.draw_repetitive_chara()
        return self.list_ennemi[player_to_attack]
    
    def draw_repetitive_chara(self):
        self.screen.fill((0,100,20))
        self.draw_background()
        self.draw_ennemi()
        self.draw_player()
        pygame.draw.rect(self.screen, (0,0,0), (0,530,800,70), 0)
        self.update_screen()
    
    def open_bag_window(self, player):
                #Bag Window
        bag_image = Image('graphics/inventory.png')
        bag_image.change_size(0.4*WIDTH, 0.5*HEIGHT)
        bag_image_desc_bar = Image('graphics/bar1.png')
        bag_image_desc_bar.change_size(WIDTH, HEIGHT*0.09)
        
        self.BagWindow = Window(width=bag_image.rect.w, height=bag_image.rect.h, left= 0.6*WIDTH, top=0.5*HEIGHT, moveable=False)
        self.BagWindow.appendBGImage(bag_image)
        self.BagWindow_desc = Window(width=bag_image_desc_bar.rect.w, height=bag_image_desc_bar.rect.h, left=0, top=0.415*HEIGHT, moveable=False)
        self.BagWindow_desc.appendBGImage(bag_image_desc_bar)
        
        
        bag = player.get_bag()
        for y in bag:
            if y != None:
                self.BagWindow.appendItem(y)
        menu_ON = True
        while menu_ON:
            
            self.BagWindow_desc.update(self.screen, self.cursor)
            self.BagWindow.update(self.screen, self.cursor)
            self.cursor.update()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu_ON = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.BagWindow != None and self.BagWindow.collide(self.cursor):
                            item = self.BagWindow.collide(self.cursor)
                            player.set_specific_parameter(item.get_type_value())
                            menu_ON = False
                            self.BagWindow.remove_item(item)
        self.draw_repetitive_chara()
     
    def open_dialog_window(self, player):
                #Bag Window
        bag_image = Image('graphics/inventory.png')
        bag_image.change_size(0.4*WIDTH, 0.5*HEIGHT)
        bag_image_desc_bar = Image('graphics/bar1.png')
        bag_image_desc_bar.change_size(WIDTH, HEIGHT*0.09)
        self.attack_Window = Window(width=bag_image.rect.w, height=bag_image.rect.h, left= 0.6*WIDTH, top=0.5*HEIGHT, moveable=False)
        self.attack_Window.appendBGImage(bag_image)
        self.BagWindow_desc = Window(width=bag_image_desc_bar.rect.w, height=bag_image_desc_bar.rect.h, left=0, top=0.415*HEIGHT, moveable=False)
        self.BagWindow_desc.appendBGImage(bag_image_desc_bar)
        
        attack = player.get_list_attack()
        j=50 
        for y in attack:
            if y != None:
                attack_props = attack[y]
                item = Item(image=load_image('graphics/item/armor/2301a.gif'),Type=attack_props[0],name=attack_props[0],desc=attack_props[0], left=50, top=j, width=124, height=24, value=80)
                self.attack_Window.appendItem(item)
                j +=20
        menu_ON = True
        while menu_ON:
            
            self.BagWindow_desc.update(self.screen, self.cursor)
            self.attack_Window.update(self.screen, self.cursor)
            self.cursor.update()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu_ON = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.attack_Window.collide(self.cursor):
                            attack_item = self.attack_Window.collide(self.cursor)
                            attack = attack_item.get_type_value()
                            #player.set_specific_parameter(item.get_type_value())
                            list_action_player = [player, attack, self.choose_player_to_Attack()]
                            self.list_action.append(list_action_player)
            
                            menu_ON = False
                            #self.attack_Window.remove_item(item)
        self.draw_repetitive_chara()
         
            
#pygame.init()
#pygame.mixer.init()
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode([WIDTH, HEIGHT],RESIZABLE)
#pygame.display.set_caption("AlChater AlMa7doud ")
#test_image = load_image('graphics/item/armor/2301a.gif')
#jugador1 = Personaje("Amine",velocidad,WIDTH,HEIGHT,"Graphics/charasets/char.png", "Graphics/battle\party/felix/Felix_Axe_Back.gif", "Graphics/battle\party/felix/Felix_Axe_Back.gif")
#jugador1.add_item_to_bag(Item(image=test_image, name="fista", desc="test1", left=10, top=32, width=124, height=24, value=80,Type="Att"))
#jugador1.add_item_to_bag(Item(image=load_image('graphics/item/armor/15032a.gif'), name="srwal", desc="pourlberd", left=10, top=32+24, width=124, height=24, value=80,Type="Att"))
#jugador2 = Personaje("Anas",velocidad,WIDTH,HEIGHT,"Graphics/charasets/char.png", "Graphics/battle/party/garet/Garet_Axe_Back.gif", "Graphics/battle/party/garet/Garet_Axe_Back.gif")
#jugador3 = Personaje("Allae",velocidad,WIDTH,HEIGHT,"Graphics/charasets/char.png", "Graphics/battle/party/ivan/Ivan_lBlade_Back.gif", "Graphics/battle/party/ivan/Ivan_lBlade_Back.gif")
#jugador4 = Personaje("Dajaja", velocidad,WIDTH,HEIGHT,"Graphics/charasets/char.png", "Graphics/battle/party/jenna/Jenna_lBlade_Back.gif", "Graphics/battle/party/jenna/Jenna_lBlade_Back.gif")

#chapitre = chapitre("chapitre1.xml")
#list_player =[jugador1, jugador2, jugador3, jugador4 ]
#fight = Fight(screen, list_player, False, chapitre)
#fight.draw_main()