#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from funciones import *
from engine import HEIGHT,WIDTH


pygame.init()

class SpriteMap( pygame.sprite.Sprite ):
    def __init__(self,imagen=None, rect=None):
        pygame.sprite.Sprite.__init__( self )
        self.imagen = imagen
        self.rect = rect
        self.old_vx = 0
        self.old_vy = 0

    def update(self, screen, vx, vy, hubo_colision, perso_colision, stop_move):
        if not stop_move and not perso_colision and not hubo_colision:
            self.rect.move_ip(-vx, -vy)
        if self.imagen != None:
            screen.blit(self.imagen,self.rect)


class SpriteMap_transition(pygame.sprite.Sprite):
    def __init__(self, screen, name, place_x, place_y, height, width, start):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.place_x = place_x
        self.place_y = place_y
        self.rect = pygame.Rect(place_x, place_y, width, height)
        self.rect.move_ip(-start[0] + WIDTH / 2, -start[1] + HEIGHT / 2)

    def update(self, screen, vx, vy, hubo_colision, perso_colision, stop_move):
        if not stop_move and not perso_colision and not hubo_colision:
            self.rect.move_ip(-vx, -vy)
            print self.rect.left


class Personaje(pygame.sprite.Sprite):
    def __init__(self, name, speed, w, h, chara_sprite, chara_fight, profile):
        pygame.sprite.Sprite.__init__( self )
        self.name = name
        self.chara = cortar_chara(chara_sprite, 4, 4)
        self.image = self.chara[0][0]
        self.fight = chara_fight
        self.profile = profile
        self.rectd = self.image.get_rect()
        self.rectd.left = w/2-self.rectd.w/2
        self.rectd.top = h/2-self.rectd.h/2

        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5,-30)
        self.rect.center = (w/2, h/2+14)
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.stop_move = False
        self.vLEFT,self.vRIGHT,self.vUP,self.vDOWN=False,False,False,False

        self.Spell = None
        self.SpellRing = pygame.Rect([0,0],[30,30])
        self.SpellRing.centerx = self.rectd.centerx
        self.SpellRing.centery = self.rectd.centery+18
        self.SpellRingTimerColor = 0
        self.SpellRingColors = [(249,204,133),(249,237,133),(212,249,133),(168,249,133),(212,249,133),(249,237,133)]
        self.UsingSpell = False
        self.StartSpell = False
        self.Spellvx = 0
        self.Spellvy = 0
        self.CastingTime = 0
        self.SpellReady = False

        self.SpellCastRect = pygame.Rect((0,0),(30,5))
        self.SpellCurrenCast = pygame.Rect((0,0),(28,3))
        self.SpellCastRect.centerx = self.rect.centerx
        self.SpellCastRect.top = self.rect.bottom+7
        self.SpellCurrenCast.left = self.SpellCastRect.left+1
        self.SpellCurrenCast.top = self.SpellCastRect.top+1

        self.maxhprect = pygame.Rect((0, 0), (30, 5))
        self.hprect = pygame.Rect((0, 0), (28, 3))
        self.maxhprect.centerx = self.rect.centerx
        self.maxhprect.top = self.rect.bottom+3
        self.hprect.left = self.maxhprect.left+1
        self.hprect.top = self.maxhprect.top+1

        # Atributos del Personaje
        self.nombre = None
        self.especializacion = "Aventurero"
        self.nivel = 1
        self.str = 1;self.str_b = 0
        self.int = 1;self.int_b = 0
        self.agi = 1;self.agi_b = 0
        self.dex = 1;self.dex_b = 0
        self.vit = 1;self.vit_b = 0
        self.stat_points = 5
        self.soul_points = 0
        self.stone_points = 0
        self.atack = 10;self.atack_b = 0
        self.defense = 5;self.defense_b = 0
        self.dodge = 8;self.dodge_b = 0
        self.crit = 3;self.crit_b = 0
        self.maxhp = 500;
        self.maxhp_b = 0
        self.hp = self.maxhp
        self.maxsp = 15;self.maxsp_b = 0
        self.sp = self.maxsp
        self.exp = 0
        self.exp_nivel = 100
        self.cash = 100
        self.bag = []
        self.list_Attack = {0: ['Attack du tigre', 50], 1: ['Attack de sara9 zit', 20], 2: ['Attack na3ssa', 30]}
        for i in range(30):
            self.bag.append(None)
        self.Equipo()
# Equipo [1-BODY,2-R,3-HEAD,4-GLOBE,5-LEGS,6-SHOES,7-RING1,8-RING2,9-NECKLACE]
    def get_list_attack(self):
        return self.list_Attack

    def get_bag(self):
        return self.bag

    def get_name(self):
        return self.name

    def get_sp(self):
        return self.sp

    def getProfile(self):
        return self.profile

    def subir_attack(self, valeur_perte):
        self.hp = self.hp - valeur_perte
        if self.hp < 0:
            self.hp = 0

    def Equipo(self):
        self.equip = []
        for i in range(9):
            self.equip.append(None)

    def get_hp(self):
        return self.hp

    def set_def_fight(self):
        self.defense_b += 50

    def get_def_fight(self):
        return int(self.defense_b)

    def get_att_fight(self):
        return self.atack_b

    def set_att_fight(self):
        self.atack_b += 50

    def get_attack(self):
        return self.atack

    def set_param_fight(self):
        self.str_b = 0
        self.int_b = 0
        self.agi_b = 0
        self.dex_b = 0
        self.vit_b = 0
        self.atack_b = 0
        self.defense_b = 0
        self.dodge_b = 0
        self.crit_b = 0

    def set_specific_parameter(self, couple_param_value):
        if couple_param_value[0] == "Att":
            self.atack_b = couple_param_value[1]
            print self.atack_b
        if couple_param_value[0] == "Def":
            self.defense_b = couple_param_value[1]
            print self.defense_b

    def set_stop_move(self, stop):
        self.stop_move = stop

    def HpBarsUpdate(self, screen):
        pygame.draw.rect(screen, (52,52,52), self.maxhprect)
        pygame.draw.rect(screen, (215,94,56), self.hprect)

    def mover_demo(self, time, map, target_x, target_y):
        if map.rect.left < target_x:
            self.vx = -self.speed
            self.x = 2
            self.image = self.chara[2][time / 10 - 1]
        elif map.rect.left > target_x:
            self.vx = self.speed
            self.x = 1
            self.image = self.chara[1][time / 10 - 1]
        elif map.rect.top < target_y:
            self.vy = -self.speed
            self.x = 0
            self.image = self.chara[0][time / 10 - 1]
        elif map.rect.top > target_y:
            self.vy = self.speed
            self.x = 3
            self.image = self.chara[3][time / 10 - 1]
        elif map.rect.left == target_x:
            self.vx = 0
        elif map.rect.top == target_y:
            self.vy = 0
        #if self.vx != 0 and self.vy != 0:
        #    self.vy = 0
        #if not perso_colision:
        #    self.oldleft= self.vx
        #    self.oldtop= self.vy
        #else:
        #    if self.vx == self.oldleft and self.vy == self.oldtop:
        #        self.vx==0
        #        self.vy==0
        #        return self.image
        if self.vx == 0 and self.vy == 0:
            return self.image
        else:
            return self.chara[self.x][time / 10 - 1]

    def update(self, screen, t, mouvement, perso_colision=False):
        if not self.UsingSpell:
            if not self.stop_move:
                self.dir = self.mover(t, mouvement, perso_colision)
                if self.Spell != None:
                    if self.Spell.Delete:
                        self.DeleteSpell()
        else:
            self.MoveSpellRing()
            self.SpellRing.move_ip(self.Spellvx, self.Spellvy)
            self.Spell.Rect.center = self.SpellRing.center
            self.SpellCurrenCast.width = self.CastingTime*28.0/self.Spell.CastTime
            if self.CastingTime >= self.Spell.CastTime:
                self.SpellReady = True
            else:
                self.CastingTime += 0.025
        screen.blit(self.dir, self.rectd)
        self.HpBarsUpdate(screen)
        if self.UsingSpell:
            pygame.draw.rect(screen, (52,52,52),self.SpellCastRect)
            pygame.draw.rect(screen, (102,204,255),self.SpellCurrenCast)

        if self.SpellRingTimerColor == 59:
            self.SpellRingTimerColor = 0
        self.SpellRingTimerColor +=0.5
        #pygame.draw.rect(screen,(200,1,105),self.rectcol)
        #pygame.draw.rect(screen, (255,255,255), self.rect)

    def MoveSpellRing(self):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.Spellvx = 1.5
        if keys[K_LEFT]:
            self.Spellvx = -1.5
        if keys[K_DOWN]:
            self.Spellvy = 1.5
        if keys[K_UP]:
            self.Spellvy = -1.5
        if not ( keys[K_RIGHT] or keys[K_LEFT]):
            self.Spellvx = 0
        if not (keys[K_DOWN] or keys[K_UP] ):
            self.Spellvy = 0

    def mover(self, t, mouvement, perso_colision):
        keys = pygame.key.get_pressed()
        global_vx, global_vy = mouvement.get_vitesse()
        if keys[K_RIGHT]:
            global_vx = self.speed
            self.x = 2
            self.image = self.chara[2][0]
        if keys[K_LEFT]:
            global_vx = -self.speed
            self.x = 1
            self.image = self.chara[1][0]
        if keys[K_DOWN]:
            global_vy = self.speed
            self.x = 0
            self.image = self.chara[0][0]
        if keys[K_UP]:
            global_vy = -self.speed
            self.x = 3
            self.image = self.chara[3][0]
        if not ( keys[K_RIGHT] or keys[K_LEFT]):
            global_vx = 0
        if not (keys[K_DOWN] or keys[K_UP] ):
            global_vy = 0
        #if self.vx != 0 and self.vy != 0:
        #    self.vy = 0
        if not perso_colision:
            self.oldleft = global_vx
            self.oldtop = global_vy
        else:
            if global_vx == self.oldleft and global_vy == self.oldtop:
                global_vx == 0
                global_vy == 0
                return self.image
        mouvement.set_vitesse(global_vx, global_vy)
        if global_vx == 0 and global_vy == 0:
            return self.image
        else:
            return self.chara[self.x][t / 10 - 1]

    # a supprimer
    def atacar(self, moblist, spell=False, massive=False):
        for i in range(len(moblist)):
            if not spell:
                if self.rect.colliderect(moblist[i].rect):
                    return i+1
            else:
                if self.SpellRing.colliderect(moblist[i].rect):
                    return i+1
        return False

    def add_item_to_bag(self, item):
        i = 0
        if None in self.bag:
            while i < len(self.bag) and self.bag[i] != None:
                i += 1
            self.bag[i] = item

    def UseSpell(self):
        self.UsingSpell = True
        self.vx = 0
        self.vy = 0
        self.dir = self.chara[self.x][0]
    def DeleteSpell(self):
        self.SpellRing.centerx = self.rectd.centerx
        self.SpellRing.centery = self.rectd.centery+18
        self.UsingSpell = False
        self.Spellvx = 0
        self.Spellvy = 0
        self.CastingTime = 0
        self.SpellReady = False
        self.StartSpell = False
        self.Spell = None
    def dano(self):
        return random.randint(self.atack/2,self.atack)
    def SpellRingUpdate(self, screen):
        color = self.SpellRingColors[int(self.SpellRingTimerColor)/10]
        pygame.draw.ellipse(screen,color,self.SpellRing, 3)

    def SubirNivel(self):
        self.nivel += 1
        self.stat_points += 5
        self.atack +=4
        self.defense += 2
        self.maxhp += self.nivel*6
        self.hp = self.maxhp
        self.maxsp += self.nivel*2-2
        self.sp = self.maxsp
        self.exp = self.exp-self.exp_nivel
        self.exp_nivel = self.exp_nivel*3/2


class Item:
    def __init__(self, ID, rect=None):
        self.ID = ID
        item = self.CargarItem()
        self.tipo = item[1]
        self.nombre = item[2]
        self.atack = int(item[3])
        self.defense = int(item[4])
        self.maxhp = int(item[5])
        self.maxsp = int(item[6])
        self.nivel = item[7]
        self.cant = int(item[8])
        self.fx = item[9]
        self.image_inv = load_image("graphics/item/" + item[10][:-1] + "a.gif", alpha=1)
        self.image_des = "graphics/item/" + item[10][:-1] + "b.gif"
        self.rect_inv = rect
        self.moveable = False

    def CargarItem(self):
        ItemDB = open("ItemDataBase.txt", "r")
        for item in ItemDB:
            i = item.split('\t')
            if str(i[0]) == str(self.ID):
                return i

    def update(self, screen, image, j, hubo_colision):
        if not hubo_colision:
            self.rect_inv.move_ip(-j.vx, -j.vy)
        screen.blit(image, self.rect_inv)


class Personnage_non_joeur(pygame.sprite.Sprite):
    def __init__(self, id, name, image, list_dialogues, start, start_perso_principal):
        pygame.sprite.Sprite.__init__( self )
        self.nom = name
        self.id = id
        self.status = "Normal"
        self.sprite = cortar_chara(image, 4, 4)
        self.nSprite = 0
        self.image = self.sprite[0][0]
        self.rect = self.image.get_rect()
        self.rect.left = start[0]
        self.rect.top = start[1]
        self.oldleft = 0
        self.oldtop = 0
        self.caminar = False
        self.vx = 0
        self.vy = 0
        self.speed = 2
        self.reached_x = False
        self.reached_y = False
        self.dialogues = list_dialogues
        self.rect.move_ip(-start_perso_principal[0] + WIDTH / 2, -start_perso_principal[1] + HEIGHT / 2)

    def get_list_dialogues(self):
        return self.dialogues

    def get_name(self):
        return str(self.nom)

    def update(self, screen, mouvement, time, hubo_colision, player_col, col, stop):
        a = random.randint(1,400)
        if a <= 9:
            self.caminar = False
            self.vx, self.vy = 0, 0
        elif a == 400 and not stop:
            self.caminar = True
            orientacion = random.choice(["x","y"])
            direccion = random.choice([-2,2])
            if orientacion == "x":
                self.vy = 0
                self.vx = direccion
            elif orientacion == "y":
                self.vx = 0
                self.vy = direccion
            if self.vx == -2:
                self.nSprite = 1
                self.image = self.sprite[1][0]
            elif self.vx:
                self.nSprite = 2
                self.image = self.sprite[2][0]
            elif self.vy == -2:
                self.nSprite = 3
                self.image = self.sprite[3][0]
            else:
                self.nSprite = 0
                self.image = self.sprite[0][0]

        if not hubo_colision and not player_col:
            (self.oldleft, self.oldtop) = (self.rect.left, self.rect.top)
            if col:
                screen.blit(self.image, self.rect)
            else:
                global_vx, global_vy = mouvement.get_vitesse()
                self.rect.move_ip(-global_vx + self.vx, -global_vy + self.vy)
                if self.vx != 0 or self.vy != 0:
                    screen.blit(self.sprite[self.nSprite][time / 10 - 1], self.rect)
                else:
                    screen.blit(self.image, self.rect)
        else:
            (self.rect.left, self.rect.top) = (self.oldleft, self.oldtop)
            if hubo_colision:
                if col:
                    screen.blit(self.image, self.rect)
                else:
                    self.rect.move_ip(self.vx, self.vy)
                    if self.vx != 0 or self.vy != 0:
                        screen.blit(self.sprite[self.nSprite][time / 10 - 1], self.rect)
                    else:
                        screen.blit(self.image, self.rect)
            if player_col:
                screen.blit(self.image, self.rect)

    def update_demo(self, screen, t, mouvement, map, target_x, target_y, perso_colision=False):
        self.dir = self.mover(t, mouvement, map, target_x, target_y)
        screen.blit(self.dir, self.rect)

    def mover(self, t, mouvement, map, target_x, target_y):
        global_vx, global_vy = mouvement.get_vitesse()
        if map.rect.left < target_x:
            global_vx = -self.speed
            self.x = 1
            self.image = self.sprite[1][0]
        elif map.rect.left > target_x:
            global_vx = self.speed
            self.x = 2
            self.image = self.sprite[2][0]
        elif map.rect.top < target_y:
            global_vy = -self.speed
            self.x = 3
            self.image = self.sprite[3][0]
        elif map.rect.top > target_y:
            global_vy = self.speed
            self.x = 0
            self.image = self.sprite[0][0]
        if map.rect.left == target_x:
            global_vx = 0
            self.reached_x = True
        if map.rect.top == target_y:
            global_vy = 0
            self.reached_y = True
        #if self.vx != 0 and self.vy != 0:
        #    self.vy = 0
        #if not perso_colision:
        #    self.oldleft= self.vx
        #    self.oldtop= self.vy
        #else:
        #    if self.vx == self.oldleft and self.vy == self.oldtop:
        #        self.vx==0
        #        self.vy==0
        #        return self.image
        mouvement.set_vitesse(global_vx, global_vy)
        if global_vx == 0 and global_vy == 0:
            return self.image
        else:
            return self.sprite[self.x][t / 10 - 1]
