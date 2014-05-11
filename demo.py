__author__ = 'asasas333_3'
import sys, pygame
from pygame.locals import *
from xml.dom import minidom, Node
from gui import *
from maps import *
from test import Mouvement
from engine import WIDTH, HEIGHT, velocidad, Max_Number_Conversation
from action import Action
from chapitre import Chapitre
from fight import Fight

class Demo:

    def __init__(self, screen, demo):
        self.name = demo
        self.list_personnages = {}
        self.list_group_move = []
        self.list_ennemies = {}
        self.pivot = 1
        self.sequence = {}
        self.creer_map()

    def set_action(self, action):
        self.action = action

    def creer_map(self):
        xmlMap = minidom.parse("demo/"+self.name)
        nPrincipal = xmlMap.childNodes[0]
        for i in range(len(nPrincipal.childNodes)):
            if nPrincipal.childNodes[i].nodeType == 1:
                if nPrincipal.childNodes[i].nodeName == "personnages":
                    npersonnages = nPrincipal.childNodes[i]
                    self.parse_param_personnage(npersonnages)
                if nPrincipal.childNodes[i].nodeName == "scenario":
                    nscenario = nPrincipal.childNodes[i]
                    self.parse_param_scenario(nscenario)


    def parse_param_personnage(self, node_personnages):

        for i in range(len(node_personnages.childNodes)):
            if node_personnages.childNodes[i].nodeType == 1:
                if node_personnages.childNodes[i].nodeName == "personnage":
                    npersonnage = node_personnages.childNodes[i]
                    id_perso = npersonnage.attributes.get("id").value
                    name = npersonnage.attributes.get("name").value
                    image = npersonnage.attributes.get("image").value
                    for i in range(len(npersonnage.childNodes)):
                        if npersonnage.childNodes[i].nodeType == 1:
                            if npersonnage.childNodes[i].nodeName == "dialogues":
                                ndialogues = npersonnage.childNodes[i]
                                list_dialogues=self.parse_param_dialogues(ndialogues)
                    attribut = [id_perso,name,image,list_dialogues]
                    self.list_personnages[id_perso] = attribut
                if node_personnages.childNodes[i].nodeName == "scenario":
                    nscenario = node_personnages.childNodes[i]
                    name = npersonnage.attributes.get("name").value
                    image = npersonnage.attributes.get("image").value
                    for i in range(len(npersonnage.childNodes)):
                        if npersonnage.childNodes[i].nodeType == 1:
                            if npersonnage.childNodes[i].nodeName == "dialogues":
                                ndialogues = npersonnage.childNodes[i]
                                list_dialogues=self.parse_param_dialogues(ndialogues)
                        attribut = [id_perso,name,image,list_dialogues]
                        self.list_personnages[id_perso] = attribut


    def parse_param_dialogues(self, ndialogues):
        # param lie a la scene
        list_dialoques={}
        for i in range(len(ndialogues.childNodes)):
            if ndialogues.childNodes[i].nodeType == 1:
                if ndialogues.childNodes[i].nodeName == "dialogue":
                    index = int(ndialogues.childNodes[i].attributes.get("index").value)
                    type = ndialogues.childNodes[i].attributes.get("type").value
                    conversation = ndialogues.childNodes[i].childNodes[0].data
                    list_dialoques[index]=[type,conversation]
        return list_dialoques

    def parse_param_scenario(self, nscenario):
        # param lie a la scene
        for i in range(len(nscenario.childNodes)):
            if nscenario.childNodes[i].nodeType == 1:
                if nscenario.childNodes[i].nodeName == "map":
                    nmap= nscenario.childNodes[i]
                    self.id_map_path = nmap.attributes.get("name").value
                if nscenario.childNodes[i].nodeName == "music":
                    nmusic= nscenario.childNodes[i]
                    self.id_music_path = nmusic.attributes.get("path").value
                if nscenario.childNodes[i].nodeName == "sequence":
                    nsequence = nscenario.childNodes[i]
                    self.parse_param_sequence(nsequence)

    def parse_param_move_groupe(self, nmove_groupe):
        # param lie a la scene
        for i in range(len(nmove_groupe.childNodes)):
            if nmove_groupe.childNodes[i].nodeType == 1:
                if nmove_groupe.childNodes[i].nodeName == "perso":
                    nperso= nmove_groupe.childNodes[i]
                    perso_id = nperso.attributes.get("personnage_id").value
                    self.list_group_move.append(perso_id)

    def parse_list_ennemies(self, node_ennemies):
        for i in range(len(node_ennemies.childNodes)):
            if node_ennemies.childNodes[i].nodeType == 1:
                if node_ennemies.childNodes[i].nodeName == "ennemi":
                    node_ennemie = node_ennemies.childNodes[i]
                    ennemi_name = node_ennemie.attributes.get("name").value
                    ennemi_image = node_ennemie.attributes.get("image").value
                    ennemi_maxhp = node_ennemie.attributes.get("maxhp").value
                    ennemi_maxsp = node_ennemie.attributes.get("maxsp").value
                    ennemi_attack = node_ennemie.attributes.get("attack").value
                    ennemi_defense = node_ennemie.attributes.get("defense").value

                    for i in range(len(node_ennemie.childNodes)):
                        if node_ennemie.childNodes[i].nodeType == 1:
                            if node_ennemie.childNodes[i].nodeName == "attacks":
                                node_attacks = node_ennemie.childNodes[i]
                                list_attacks=self.parse_list_attacks(node_attacks)
                                ennemi = [ennemi_name, ennemi_image, ennemi_maxhp, ennemi_maxsp, ennemi_attack, ennemi_defense, list_attacks]
                if self.list_ennemies:
                    index = len(self.list_ennemies)
                else:
                    index = 0
                self.list_ennemies[index] = ennemi

    def parse_list_attacks(self, node_attacks):
        list_attack={}
        for i in range(len(node_attacks.childNodes)):
            if node_attacks.childNodes[i].nodeType == 1:
                if node_attacks.childNodes[i].nodeName == "attack":
                    attack_name = node_attacks.childNodes[i].attributes.get("name").value
                    attack_value = node_attacks.childNodes[i].attributes.get("value").value
                    attack=[attack_name, attack_value]
                    index = len(list_attack)
                    list_attack[index] = attack
        return list_attack

    def parse_param_sequence(self,nsequence):
        pivot = 0
        for i in range(len(nsequence.childNodes)):
            if nsequence.childNodes[i].nodeType == 1:
                pivot=pivot+1
                if nsequence.childNodes[i].nodeName == "move":
                    nmove= nsequence.childNodes[i]
                    self.id_perso = nmove.attributes.get("personnage_id").value
                    self.target_x = nmove.attributes.get("target_x").value
                    self.target_y = nmove.attributes.get("target_y").value
                    self.sequence[pivot]=["move", self.id_perso, self.target_x, self.target_y]
                if nsequence.childNodes[i].nodeName == "move_groupe":
                    self.list_group_move
                    nmove_groupe= nsequence.childNodes[i]
                    self.target_x = nmove_groupe.attributes.get("target_x").value
                    self.target_y = nmove_groupe.attributes.get("target_y").value
                    self.decal = nmove_groupe.attributes.get("decalage").value
                    self.parse_param_move_groupe(nmove_groupe)
                    self.sequence[pivot]=["move_groupe", self.list_group_move, self.target_x, self.target_y, self.decal]
                if nsequence.childNodes[i].nodeName == "talk":
                    ntalk= nsequence.childNodes[i]
                    self.id_perso = ntalk.attributes.get("personnage_id").value
                    id_position = ntalk.attributes.get("position").value
                    self.sequence[pivot]=["talk", self.id_perso, id_position]
                if nsequence.childNodes[i].nodeName == "jump":
                    njump= nsequence.childNodes[i]
                    self.id_perso = njump.attributes.get("personnage_id").value
                    self.sequence[pivot]=["jump", self.id_perso]
                if nsequence.childNodes[i].nodeName == "fight":
                    nfight= nsequence.childNodes[i]
                    id_perso = nfight.attributes.get("personnage_id").value
                    place = nfight.attributes.get("place").value
                    for i in range(len(nfight.childNodes)):
                        if nfight.childNodes[i].nodeType == 1:
                            if nfight.childNodes[i].nodeName == "ennemies":
                                node_ennemies = nfight.childNodes[i]
                                self.parse_list_ennemies(node_ennemies)
                    self.sequence[pivot]=["fight", id_perso, self.list_ennemies, place ]

    def check_move(self,map,target_x,target_y):
        if map.rect.left == target_x and map.rect.top == target_y:
            return True
        return False

    def get_id_mob(self,perso, MapTest):
        i=0
        perso = self.list_personnages.__getitem__(perso)
        while MapTest.mobs[i].id != perso[0]:
            i=i+1
        return i


    def run_sequence(self, screen, time,mouvement,MapTest):
        if len(self.sequence) > 0:
            action = self.sequence.get(self.pivot)
            if action[0] == "move":
                list = []
                i = self.get_id_mob(action[1],MapTest)
                list.append(MapTest.mobs[i])
                target_x = int(action[2].strip())
                target_y = int(action[3].strip())
                while(not self.check_move(MapTest.mapa,target_x,target_y)):
                    time+=1
                    clock.tick(60)
                    if time>40:
                        time=0
                    trans_colision = pygame.sprite.spritecollideany(MapTest.mobs[i], MapTest.TransGroup)
                    if trans_colision:
                        chapitre = Chapitre(trans_colision.name+".xml")
                        MapTest = Mapa(trans_colision.name+".tmx", chapitre.list_personnages, screen)
                    screen.fill((0,0,0))
                    cursor.update()
                    MapTest.update(screen, mouvement, False, False, False)
                    MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=True,perso_demo=list)
                    MapTest.TransUpdate(screen, mouvement, time, False, False)
                    hubo_colision = pygame.sprite.spritecollideany(MapTest.mobs[i], MapTest.colisionesGroup)
                    MapTest.mobs[i].update_demo(screen,time,mouvement,MapTest,target_x,target_y)
                    screen.blit(MapTest.OverMap.imagen, MapTest.mapa.rect)
                    pygame.display.update()
            elif action[0] == "move_groupe":
                list = []
                list_perso = action[1]
                for perso in list_perso:
                    i = self.get_id_mob(perso,MapTest)
                    list.append(MapTest.mobs[i])
                target_x = int(action[2].strip())
                target_y = int(action[3].strip())
                while(not self.check_move(MapTest.mapa,target_x,target_y)):
                    time+=1
                    clock.tick(60)
                    if time>40:
                        time=0
                    trans_colision = pygame.sprite.spritecollideany(MapTest.mobs[i], MapTest.TransGroup)
                    if trans_colision:
                        chapitre = Chapitre(trans_colision.name+".xml")
                        MapTest = Mapa(trans_colision.name+".tmx", chapitre.list_personnages, screen)
                    screen.fill((0,0,0))
                    cursor.update()
                    MapTest.update(screen, mouvement, False, False, False)
                    MapTest.MobsUpdate(screen, mouvement , time, False, False, demo=True,perso_demo=list)
                    MapTest.TransUpdate(screen, mouvement, time, False, False)
                    hubo_colision = pygame.sprite.spritecollideany(MapTest.mobs[i], MapTest.colisionesGroup)
                    self.action.move_groupe(list,screen,time,mouvement,MapTest, int(action[2]), int(action[3]), action[4])
                    screen.blit(MapTest.OverMap.imagen, MapTest.mapa.rect)
                    pygame.display.update()
            elif action[0] == "talk":
                i = self.get_id_mob(action[1],MapTest)
                self.action.Talk(MapTest.mobs[i],time, int(action[2]))
            elif action[0] == "jump":
                i = self.get_id_mob(action[1],MapTest)
                self.action.jump(MapTest,screen, mouvement , time,stop=True, demo=True,perso=MapTest.mobs[i])
            elif action[0] == "fight":
                list = []
                i = self.get_id_mob(action[1],MapTest)
                jugador1 = Personaje(MapTest.mobs[i].get_name(),velocidad,WIDTH,HEIGHT,MapTest.mobs[i].image_path, "Graphics/battle\party/felix/Felix_Axe_Back.gif", "Graphics/battle\party/felix/Felix_Axe_Back.gif")
                list.append(jugador1)
                fight = Fight(screen, list,action[2], None, action[3])
                fight.draw_main()
            self.sequence.pop(self.pivot)
            self.pivot =self.pivot+1
        return len(self.sequence)


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT],RESIZABLE)
pygame.display.set_caption("AlChater AlMa7doud ")
time=0
mouvement = Mouvement()
cursor = Cursor()
demo = Demo(screen, "demo1.xml")
MapTest = Mapa(demo.id_map_path, demo.list_personnages, screen)
action = Action(screen, cursor, mouvement, MapTest)
player = demo.list_personnages.__getitem__("reine")
demo.set_action(action)

while True:
    time+=1
    clock.tick(60)
    if time>40:
        time=0
    list_perso = MapTest.mobs[1]
    screen.fill((0,0,0))
    cursor.update()
    MapTest.update(screen, mouvement, False, False, False)
    MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=False,perso_demo=None)
    #list_perso.update_demo(screen,time,mouvement,MapTest.mapa,50,-300)
    pygame.display.update()
    screen.blit(MapTest.OverMap.imagen, MapTest.mapa.rect)
    while (demo.run_sequence(screen, time,mouvement,MapTest) > 0):
        time+=1
        clock.tick(60)
        if time>40:
            time=0
        screen.fill((0,0,0))
        cursor.update()
        MapTest.update(screen, mouvement, False, False, False)
        MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=True,perso_demo=None)
        MapTest.TransUpdate(screen, mouvement, time, False,False)
        demo.run_sequence(screen, time,mouvement,MapTest)
        pygame.display.update()
    #if MapTest.mapa.rect.top != 2 and MapTest.mapa.rect.left != 2:
        #jugador1.mover_demo(time,MapTest.mapa, 2,2)
    #pygame.display.update()
    pygame.quit()
    sys.exit()