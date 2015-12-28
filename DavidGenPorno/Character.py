import sys
import pygame
from pygame import *
from SpriteRemix import *


class Character():
    def __init__(self, name = "", health = 0, sprite = CharacterSprite(pygame.image.load("Assets\\sprites\\ass.png"))):
        self.name = name
        self.health = health
        self.sprite = sprite

class PlayerCharacter(Character):
    def __init__(self, sprite, name="", health = 100):
        super().__init__(name, health, sprite)
        self.lastHit = 0
        self.numJumps = 2
        self.ammo = 3

class NPC(Character):
    def __init__(self, sprite, name="", health = 100, hostile = True):
        super().__init__(name, health, sprite)
        self.hostile = hostile
        self.lastHit = 0
