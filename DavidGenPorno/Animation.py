import pygame
from pygame import *
import SpriteRemix

class Animation():
    def __init__(self):
        self.inuse = []
        self.count = -1
    def animate(self, sprite, now):
        tempLoc = sprite.rect.bottomleft
        if isinstance(sprite, SpriteRemix.CharacterSprite):
            tempLoc = sprite.rect.bottomleft
            if sprite.name == "pc":
                #TODO: A whole fuckin' lot. State handling for PC as well as sprites for PC, etc. etc. etc.
                if sprite.stateVal == 0: #idle animation
                    if now % 1500 > 750:                    
                        sprite.setImage(self.inuse[sprite.id][0])
                    elif now % 1500 > 400 or now % 1500 <= 150:
                        sprite.setImage(self.inuse[sprite.id][1])
                    else:
                        sprite.setImage(self.inuse[sprite.id][2])
                        
            elif sprite.name == "notzigrunt":
                if sprite.stateVal == 0:
                    if now % 1500 < 250:
                        
                        sprite.setImage(self.inuse[sprite.id][1])
                        
                    else:
                        sprite.setImage(self.inuse[sprite.id][0])
                else:
                    sprite.setImage(self.inuse[sprite.id][2])

            if sprite.xflip:
                sprite.setImage(transform.flip(sprite.image, True, False))

            sprite.rect.bottomleft = tempLoc


        elif isinstance(sprite, SpriteRemix.Projectile):
            tempLoc = sprite.rect.center
            if sprite.stateVal == 1:
                tempImage = transform.rotate(self.inuse[sprite.id][0],-90)
                self.inuse[sprite.id][0] = tempImage = transform.rotate(self.inuse[sprite.id][1],-90)
                self.inuse[sprite.id][1] = tempImage
                sprite.setImage(self.inuse[sprite.id][0])
            sprite.rect.center = tempLoc
                                     
    def load(self, sprite):

        #look for spot in inuse to store new sprite data, if no empty spots, append to the end
        overWrite = 0
        for i in range(len(self.inuse)):
            if not self.inuse[i]:
                sprite.id = i
                overWrite = i
        if not overWrite:
            self.count += 1
            sprite.id = self.count
        
        if isinstance(sprite, SpriteRemix.CharacterSprite):
            if sprite.name == "pc":
                pc = [\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle1.png").convert_alpha(),(180,270)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle2.png").convert_alpha(),(180,273)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle3.png").convert_alpha(),(180,276))\
                ]
                if overWrite: #0 is PC and is never deleted
                    self.inuse[overWrite] = pc
                else:
                    self.inuse.append(pc)

            elif sprite.name == "notzigrunt":
                notzigrunt = [\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigrunt.png").convert_alpha(),(180,270)),\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigruntidle2.png").convert_alpha(),(180,270)),\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigruntdead.png").convert_alpha(),(270,180)),\
                ]
                if overWrite:
                    self.inuse[overWrite] = notzigrunt
                else:
                    self.inuse.append(notzigrunt)
        elif isinstance(sprite, SpriteRemix.Projectile):
            if sprite.name == "pcdefaultproj":
                pcdefaultproj = [\
                    transform.scale(image.load("Assets\\sprites\\projectiles\\pcdefaultproj1.png").convert_alpha(),(135,135)),\
                    transform.scale(image.load("Assets\\sprites\\projectiles\\pcdefaultproj2.png").convert_alpha(),(180,180))\
                ]
                if overWrite:
                    self.inuse[overWrite] = pcdefaultproj
                else:
                    self.inuse.append(pcdefaultproj)
        else:
            self.inuse.append([])


    
