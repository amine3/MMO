#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
from pygame.locals import *
from xml.dom import minidom, Node
from sprite import *
from funciones import *
from engine import WIDTH, HEIGHT


class Chapitre:
    def __init__(self, nom):
        self.nom = nom
        self.list_ennemies = {}
        self.scene_path = ""
        self.list_personnages = {}
        self.creer_chapitre()
        
        
    def creer_chapitre(self):
        xmlMap = minidom.parse("chapitres/"+self.nom)
        nPrincipal = xmlMap.childNodes[0]
        for i in range(len(nPrincipal.childNodes)):
            if nPrincipal.childNodes[i].nodeType == 1:
                if nPrincipal.childNodes[i].nodeName == "fight":
                    nFight = nPrincipal.childNodes[i]
                    self.parse_param_fight(nFight)
                elif nPrincipal.childNodes[i].nodeName == "personnages":
                    npersonnages = nPrincipal.childNodes[i]
                    self.parse_param_personnage(npersonnages)
                    
    def parse_param_fight(self, node_fight):
        # param lie a la scene
        for i in range(len(node_fight.childNodes)):
            if node_fight.childNodes[i].nodeType == 1:
                if node_fight.childNodes[i].nodeName == "scene":
                    self.scene_path = node_fight.childNodes[i].attributes.get("source").value
                elif node_fight.childNodes[i].nodeName == "ennemies":
                    node_ennemies = node_fight.childNodes[i]
                    self.parse_list_ennemies(node_ennemies)
    
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

    def get_scene_path(self):
        return self.scene_path
    
    def get_list_ennemies(self):
        return self.list_ennemies

