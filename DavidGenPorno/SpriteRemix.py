import pygame
from pygame import sprite
from Movement import *
from Animation import *

class SpriteRemix(sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.xcoast = 0
        self.ycoast = 0
        self.id = 0

    def setImage(self, image):
        self.image = image
        self.rect = image.get_rect()


class Doodad(SpriteRemix):
    def __init__(self, image):
        super().__init__(image)
        self.velocity = [0,0]
        self.xcoast = 0
        self.ycoast = 0


class Background(SpriteRemix):
    def __init__(self, image):
        super().__init__(image)
        self.lastUpdate = 0
        self.stateVal = 0
        self.velocity = [0,0]
        #self.state = ["static","slowscroll","fastscroll"]

#NOTE: right now has no additional functionality, but that may change
class Cursor(SpriteRemix):
    def __init__(self, image):
        super().__init__(image)
                         
class CharacterSprite(SpriteRemix):

    def __init__(self, image, name = ""):
        super().__init__(image)
        self.name = name
        self.front = self.rect.right
        self.collided = False
        self.falling = False
        self.velocity = [0,0]
        self.numJumps = 1
        self.stateVal = 0
        self.lastShot = 0 #last time the unit fired a projectile
        #self.state = [idle,ready,running,attack,dead]
        self.xflip = False

class PCSprite(CharacterSprite):

    def __init__(self, image, name = ""):
        super().__init__(image, name)
        self.leftDash = 0
        self.rightDash = 0
        self.numJumps = 2
        self.stateVal = 1

class UI(SpriteRemix):
    def __init__(self, image):
        super().__init__(image)
        

class Projectile(SpriteRemix):
    def __init__(self, image, origin, dest, name="pcdefaultproj", speed=20, dmg = 20, grav = False, hostile = False, piercing = False):
        super().__init__(image)
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
