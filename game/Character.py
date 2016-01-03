import sys
import pygame
from SpriteRemix import SpriteRemix


class CharacterSprite(SpriteRemix):
    def __init__(self, name = "", health = 0):
        super().__init__()
                
        #from SpriteRemix.CharacterSprite
        self.name = name
        self.falling = False #TODO: fold into self.state
        self.velocity = [0,0]
        self.numJumps = 1
        self.stateVal = 0 #TODO: fold into self.state
        self.lastShot = 0 #last time the unit fired a projectile
        self.lastMelee = 0

        # boolean dictionary that represents the state of a character
        # (e.g. ducking and attacking, falling and dying)
        # can be added to, may add dashing, blocking, etc.
        self.state = {"idle":False,\
                      "ready":True,\
                      "attacking":False,\
                      "shooting":False,\
                      "ducking":False,\
                      "running":False,\
                      "jumping":False,\
                      "falling":False,\
                      "dying":False,\
                      "dead":False,\
                     }
        # dict of ints representing the last time an action was taken
        # allows combos of inputs
        self.last = {"ran":0,\
                      "dashed":0,\
                      "jumped":0,\
                      "meleed":0,\
                      "shot":0,\
                    }
        
        self.xflip = False
        self.idleTime = 0
        
        self.name = name
        self.health = health

    def setImage(self, image):
        self.image = image
        self.rect = image.get_rect()

class PlayerCharacterSprite(CharacterSprite):
    def __init__(self, name="pc", health = 100):
        super().__init__(name, health)
        self.lastHit = 0
        self.numJumps = 2
        self.ammo = 3

        #from SpriteRemix.PCSprite
        self.leftDash = 0
        self.rightDash = 0
        self.stateVal = 1

class EnemyCharacterSprite(CharacterSprite):
    def __init__(self, name="", health = 100, hostile = True):
        super().__init__(name, health)
        self.hostile = hostile
        self.lastHit = 0
