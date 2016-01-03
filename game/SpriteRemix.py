import pygame
from pygame import sprite
from Movement import *
from Animation import *

class SpriteRemix(sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets\\sprites\\default.png")
        self.rect = self.image.get_rect()
        self.velocity = [0,0]
        self.xcoast = 0
        self.ycoast = 0
        self.xflip = False
        self.id = 0
        self.visible = True

    def setImage(self, image):
        self.image = image
        self.rect = image.get_rect()


class Doodad(SpriteRemix):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.velocity = [0,0]
        self.xcoast = 0
        self.ycoast = 0


class Background(SpriteRemix):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.lastUpdate = 0
        self.stateVal = 0
        self.velocity = [0,0]
        #self.state = ["static","slowscroll","fastscroll"]

#NOTE: right now has no additional functionality, but that may change
class Cursor(SpriteRemix):
    def __init__(self, image):
        super().__init__()
        self.image = image


class UI(SpriteRemix):
    def __init__(self, image):
        super().__init__()
        self.image = image
        

class Projectile(SpriteRemix):
    def __init__(self, origin, dest, name="pcdefaultproj", speed=20, dmg = 20, grav = False, hostile = False, piercing = False):
        super().__init__()
        self.name = name
        self.origin = origin
        self.dest = dest
        self.speed = speed
        self.velocity = Movement.shoot(self)
        self.grav = grav
        self.falling = True
        self.hostile = hostile
        self.dmg = dmg
        self.piercing = piercing
        self.stateVal = 1
        #self.state = ["static","spinning","sinewave",...

class Weapon(SpriteRemix):
    def __init__(self):
        super().__init__()
        self.name = "weapon"
        self.falling = True
        self.hostile = False
        self.dmg = 40
        self.stateVal = 1
        #self.state = ["static","spinning","sinewave",...
