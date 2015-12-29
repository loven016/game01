import sys
import pygame
from pygame import sprite


class CharacterSprite(sprite.Sprite):
    def __init__(self, name = "", health = 0, img = "Assets\\sprites\\ass.png"):
        super().__init__()
        imgSprite = pygame.image.load(img)
        
        #from SpriteRemix
        self.image = imgSprite
        self.rect = self.image.get_rect()
        self.xcoast = 0
        self.ycoast = 0
        self.id = 0
        
        #from SpriteRemix.CharacterSprite
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
        
        self.name = name
        self.health = health

    def setImage(self, image):
        self.image = image
        self.rect = image.get_rect()

class PlayerCharacterSprite(CharacterSprite):
    def __init__(self, img, name="", health = 100):
        super().__init__(name, health, img)
        self.lastHit = 0
        self.numJumps = 2
        self.ammo = 3
        
        #from SpriteRemix.PCSprite
        self.leftDash = 0
        self.rightDash = 0
        self.stateVal = 1

class EnemyCharacterSprite(CharacterSprite):
    def __init__(self, img, name="", health = 100, hostile = True):
        super().__init__(name, health, img)
        self.hostile = hostile
        self.lastHit = 0
