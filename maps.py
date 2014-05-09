#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
from xml.dom import minidom

from sprite import *
from funciones import *
from engine import WIDTH, HEIGHT

#import base64
#import gzip
#import StringIO

# Clases
# ---------------------------------------------------------------------

class Mapa:
    def __init__(self, nombre, list_personnages, screen):

        self.nombre = nombre
        self.start = None
        self.capas = []
        self.mobs = []
        self.transition = []
        self.list_personnages = list_personnages
        self.cargar_mapa()  # Inicializa los valores desde el xml.

        # Group monsters
        self.MobGroup = pygame.sprite.RenderUpdates()
        for i in range(len(self.mobs)):
            list = self.mobs[i]
            id = list[0]
            self.start_mobs = (list[1], list[2])
            if not self.start:
                self.start = self.start_mobs
            perso = list_personnages[id]
            Mob = Personnage_non_joeur(perso[0], perso[1], perso[2], perso[3], self.start_mobs, self.start)
            self.mobs[i] = Mob
            self.MobGroup.add(Mob)

        # Group Transtions
        self.TransGroup = pygame.sprite.RenderUpdates()
        for i in range(len(self.transition)):
            list = self.transition[i]
            trans = SpriteMap_transition(screen, list[0], list[1], list[2], list[3], list[4], self.start)
            self.transition[i] = trans
            self.TransGroup.add(trans)
        self.crear_mapa()

        # Extrae valores mapa desde XML.

    def cargar_mapa(self):
        xmlMap = minidom.parse("maps/" + self.nombre)
        nPrincipal = xmlMap.childNodes[0]

        # Tamaño mapa
        self.width = int(nPrincipal.attributes.get("width").value)
        self.height = int(nPrincipal.attributes.get("height").value)
        tset = []

        for i in range(len(nPrincipal.childNodes)):
            if nPrincipal.childNodes[i].nodeType == 1:
                if nPrincipal.childNodes[i].nodeName == "tileset":
                    if nPrincipal.childNodes[i].attributes.get("name").value != "config":
                        self.tilewidth = int(nPrincipal.childNodes[i].attributes.get("tilewidth").value)
                        self.tileheight = int(nPrincipal.childNodes[i].attributes.get("tileheight").value)
                        nombre = nPrincipal.childNodes[i].childNodes[1].attributes.get("source").value
                        nombre = extraer_nombre(nombre)
                        #self.tileset.append(nombre)
                    self.tam_tiles = (int(self.tilewidth), int(self.tileheight))
                    tset = tset + cortar_tileset("graphics/tilesets/" + nombre, self.tam_tiles)[1:]
                elif nPrincipal.childNodes[i].nodeName == "layer":
                    if nPrincipal.childNodes[i].attributes.get("name").value == "over":
                        layer = nPrincipal.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ",
                                                                                                                    "")
                        layer = decodificar(layer)  # Decodifica la lista
                        #print layer
                        layer = convertir(layer, self.width)  # Convierta en array bidimensional
                        self.capaOver = layer
                    elif nPrincipal.childNodes[i].attributes.get("name").value == "colisiones":
                        layer = nPrincipal.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ",
                                                                                                                    "")
                        layer = decodificar(layer)  # Decodifica la lista
                        #print layer
                        layer = convertir(layer, self.width)  # Convierta en array bidimensional
                        self.capaColisiones = layer
                    else:
                        layer = nPrincipal.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ",
                                                                                                                    "")
                        layer = decodificar(layer)  # Decodifica la lista
                        #print layer
                        layer = convertir(layer, self.width)  # Convierta en array bidimensional
                        self.capas.append(layer)
                elif nPrincipal.childNodes[i].nodeName == "objectgroup":
                    for j in range(len(nPrincipal.childNodes[i].childNodes)):
                        try:
                            objeto = nPrincipal.childNodes[i].childNodes[j].attributes.get("name").value
                            x = nPrincipal.childNodes[i].childNodes[j].attributes.get("x").value
                            y = nPrincipal.childNodes[i].childNodes[j].attributes.get("y").value
                            if objeto == "heroe":
                                self.start = (int(x), int(y))
                            else:
                                if nPrincipal.childNodes[i].childNodes[j].attributes.get("type"):
                                    type = nPrincipal.childNodes[i].childNodes[j].attributes.get("type").value
                                    if type == "transition":
                                        height = nPrincipal.childNodes[i].childNodes[j].attributes.get("height").value
                                        width = nPrincipal.childNodes[i].childNodes[j].attributes.get("width").value
                                        self.transition.append((objeto, int(x), int(y), int(height), int(width)))
                                else:
                                    self.mobs.append((objeto, int(x), int(y)))

                        except:
                            pass
        self.tileset = [0] + tset

    def update(self, screen, mouvement, hubo_colision, perso_colision, stop_move=False):
        if hubo_colision or perso_colision:
            self.mapa.rect.left = self.left
            self.mapa.rect.top = self.top
            self.mapa.update(screen, 0, 0, hubo_colision, perso_colision, stop_move)
            for i in range(len(self.colisiones)):
                (self.colisiones[i].rect.left, self.colisiones[i].rect.top) = self.recs[i]
        else:
            vx, vy = mouvement.get_vitesse()
            (self.left, self.top) = (self.mapa.rect.left, self.mapa.rect.top)
            self.mapa.update(screen, vx, vy, hubo_colision, perso_colision, stop_move)
            self.recs = range(len(self.colisiones))
            for i in range(len(self.colisiones)):
                self.recs[i] = (self.colisiones[i].rect.left, self.colisiones[i].rect.top)
                if not stop_move:
                    self.colisiones[i].rect.move_ip(-vx, -vy)
                    #pygame.draw.rect(screen,(200,255,105),self.ctileheight))

    def crear_mapa(self):
        self.colisionesGroup = pygame.sprite.RenderUpdates()
        self.colisiones = []
        self.mapa = pygame.Surface((self.width * self.tilewidth, self.height * self.tileheight))
        self.OverMap = pygame.Surface((self.width * self.tilewidth, self.height * self.tileheight), pygame.SRCALPHA, 32)
        self.OverMap = self.OverMap.convert_alpha()
        for i in xrange(len(self.capas)):
            for f in xrange(self.height):
                for c in xrange(self.width):
                    element = self.capas[i][f][c]
                    if element:
                        self.mapa.blit(self.tileset[element], (c * self.tilewidth, f * self.tileheight))
                        if i == 0:
                            if self.capaColisiones[f][c]:
                                rect = pygame.Rect(c * self.tilewidth, f * self.tileheight, self.tilewidth,
                                                   self.tileheight)
                                rect.move_ip(-self.start[0] + WIDTH / 2, -self.start[1] + HEIGHT / 2)
                                s = SpriteMap(rect=rect)
                                self.colisiones.append(s)
                                self.colisionesGroup.add(s)
                            if self.capaOver[f][c]:
                                self.OverMap.blit(self.tileset[self.capaOver[f][c]],
                                                  (c * self.tilewidth, f * self.tileheight))


                    else:
                        pass
        rectmap = self.mapa.get_rect()
        rectovermap = self.OverMap.get_rect()
        self.mapa = SpriteMap(self.mapa, rectmap)
        self.OverMap = SpriteMap(self.OverMap, rectovermap)
        self.capas = []
        self.capaColisiones = []
        self.capaOver = []
        self.mapa.rect.move_ip(-self.start[0] + WIDTH / 2, -self.start[1] + HEIGHT / 2)
        self.OverMap.rect.move_ip(-self.start[0] + WIDTH / 2, -self.start[1] + HEIGHT / 2)
        #for i in range(len(self.colisiones)):
        #	self.colisiones[i].move_ip(-self.start[0]+WIDTH/2, -self.start[1]+HEIGHT/2)

    def MobsUpdate(self, screen, mouvement, time, maps_col, player_col, stop=False, demo=False, perso_demo=None):
        for i in range(len(self.mobs)):
            if pygame.sprite.spritecollideany(self.mobs[i], self.colisionesGroup):
                self.mobs[i].update(screen, mouvement, time, maps_col, player_col, True, stop)
            else:
                if not demo or (demo and (perso_demo and self.mobs[i] not in  perso_demo)):
                    self.mobs[i].update(screen, mouvement, time, maps_col, player_col, False, stop)

    def TransUpdate(self, screen, mouvement, time, maps_col, player_col, stop=False, demo=False, perso_demo=None):
        vx, vy = mouvement.get_vitesse()
        for i in range(len(self.transition)):
            if not demo or (demo and self.mobs[i] != perso_demo):
                vx, vy = mouvement.get_vitesse()
                self.transition[i].update(screen, vx, vy, maps_col, player_col, stop)

    def MobsHpBarsUpdate(self, screen):
        pass
        #for m in self.mobs:
        #    m.HpBarsUpdate(screen)


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------


# Convierta una array unidimensional en una bidimensional.
def convertir(lista, col):
    nueva = []
    for i in range(0, len(lista), col):
        nueva.append(lista[i:i + col])
    return nueva


# Extrae el nombre de un archivo de una ruta.
def extraer_nombre(ruta):
    a = -1
    for i in range(len(ruta)):
        if ruta[i] == "/" or ruta[i] == "\\":
            a = i
    if a == -1:
        return ruta
    return ruta[a + 1:]


# ---------------------------------------------------------------------

def main():
    return 0


if __name__ == '__main__':
    main()
