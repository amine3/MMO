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

class Demo:

    def __init__(self, screen, demo):
        self.name = demo
        self.list_personnages = {}
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
                if nsequence.childNodes[i].nodeName == "talk":
                    ntalk= nsequence.childNodes[i]
                    self.id_perso = ntalk.attributes.get("personnage_id").value
                    self.sequence[pivot]=["talk", self.id_perso]
                if nsequence.childNodes[i].nodeName == "jump":
                    njump= nsequence.childNodes[i]
                    self.id_perso = njump.attributes.get("personnage_id").value
                    self.sequence[pivot]=["jump", self.id_perso]

    def check_move(self,map,target_x,target_y):
        if map.rect.left == target_x and map.rect.top == target_y:
            return True
        return False
    def run_sequence(self, screen, time,mouvement,MapTest):
        if len(self.sequence) > 0:
            action = self.sequence.get(self.pivot)
            i=0
            perso = self.list_personnages.__getitem__(action[1])
            while MapTest.mobs[i].nom != perso[0]:
                i=i+1
            if action[0] == "move":
                target_x = int(action[2].strip())
                target_y = int(action[3].strip())
                while(not self.check_move(MapTest.mapa,target_x,target_y)):
                    time+=1
                    clock.tick(60)
                    if time>40:
                        time=0
                    trans_colision = pygame.sprite.spritecollideany(MapTest.mobs[i], MapTest.TransGroup)
                    print MapTest.mobs[i].rect.left
                    if trans_colision:
                        chapitre = Chapitre(trans_colision.name+".xml")
                        MapTest = Mapa(trans_colision.name+".tmx", chapitre.list_personnages, screen)
                    screen.fill((0,0,0))
                    cursor.update()
                    MapTest.update(screen, mouvement, False, False, False)
                    MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=True,perso_demo=MapTest.mobs[i])
                    MapTest.TransUpdate(screen, mouvement, time, False, False)
                    MapTest.mobs[i].update_demo(screen,time,mouvement,MapTest.mapa,target_x,target_y)
                    screen.blit(MapTest.OverMap.imagen, MapTest.mapa.rect)
                    pygame.display.update()

            elif action[0] == "talk":
                self.action.Talk(MapTest.mobs[i],time)
            elif action[0] == "jump":
                self.action.jump(MapTest,screen, mouvement , time,stop=True, demo=True,perso=MapTest.mobs[i])
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
    MapTest.MobsUpdate(screen, mouvement , time, False, False,stop=True, demo=None,perso_demo=None)
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
    pygame.display.update()
