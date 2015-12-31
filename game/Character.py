import sys
import pygame
from pygame import sprite


class CharacterSprite(sprite.Sprite):
    def __init__(self, name = "", health = 0):
        super().__init__()
        
        #from SpriteRemix
        self.image = pygame.image.load("Assets\\sprites\\default.png")
        self.rect = self.image.get_rect()
        self.xcoast = 0
        self.ycoast = 0
        self.id = 0
        self.visible = True
        
        #from SpriteRemix.CharacterSprite
        self.name = name
        self.front = self.rect.right
        self.collided = False
        self.falling = False
        self.velocity = [0,0]
        self.numJumps = 1
        self.stateVal = 0
        self.lastShot = 0 #last time the unit fired a projectile
        self.lastMelee = 0
        #self.state = [idle,ready,running,attack,dead]
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
