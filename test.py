__author__ = 'asasas333_3'



class Mouvement:

    def __init__(self):
        self.global_vx = 0
        self.global_vy = 0

    def set_vitesse(self,vx,vy):
        self.global_vx = vx
        self.global_vy = vy

    def get_vitesse(self):
        return (self.global_vx,self.global_vy)