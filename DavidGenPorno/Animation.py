import pygame
from pygame import *
import SpriteRemix

class Animation():
    def __init__(self):
        self.inuse = []
        self.count = -1
    def animate(self, spritesList, now):
        
        for i in range(len(spritesList)):
            if isinstance(spritesList[i], SpriteRemix.CharacterSprite):
                tempLoc = spritesList[i].rect.bottomleft
                if spritesList[i].name == "pc":
                    #TODO: A whole fuckin' lot. State handling for PC as well as sprites for PC, etc. etc. etc.
                    if spritesList[i].stateVal == 0: #idle animation
                        if now % 1500 > 750:                    
                            spritesList[i].setImage(self.inuse[spritesList[i].id][0])
                        elif now % 1500 > 400 or now % 1500 <= 150:
                            spritesList[i].setImage(self.inuse[spritesList[i].id][1])
                        else:
                            spritesList[i].setImage(self.inuse[spritesList[i].id][2])
                            
                elif spritesList[i].name == "notzigrunt":
                    if spritesList[i].stateVal == 0:
                        if now % 1500 < 250:
                            
                            spritesList[i].setImage(self.inuse[spritesList[i].id][1])
                            
                        else:
                            spritesList[i].setImage(self.inuse[spritesList[i].id][0])
                    else:
                        spritesList[i].setImage(self.inuse[spritesList[i].id][2])

                if spritesList[i].xflip:
                    spritesList[i].setImage(transform.flip(spritesList[i].image, True, False))

                spritesList[i].rect.bottomleft = tempLoc


            elif isinstance(spritesList[i], SpriteRemix.Projectile):
                tempLoc = spritesList[i].rect.center
                if spritesList[i].stateVal == 1:
                    tempImage = transform.rotate(self.inuse[spritesList[i].id][0],-90)
                    self.inuse[spritesList[i].id][0] = tempImage = transform.rotate(self.inuse[spritesList[i].id][1],-90)
                    self.inuse[spritesList[i].id][1] = tempImage
                    spritesList[i].setImage(self.inuse[spritesList[i].id][0])
                spritesList[i].rect.center = tempLoc

            elif isinstance(spritesList[i], SpriteRemix.Background):
                if spritesList[i].stateVal == 1:
                    if now - spritesList[i].lastUpdate > 48:
                        spritesList[i].lastUpdate = now
                        spritesList[i].velocity = [1,0]
                    else:
                        spritesList[i].velocity = [0,0]
                    if spritesList[i].rect.left >= 1920:
                        spritesList[i].rect.right = 0
                                         
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
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle1.png").convert_alpha(),(144,216)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle2.png").convert_alpha(),(144,219)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle3.png").convert_alpha(),(144,221 ))\
                ]
                if overWrite: #0 is PC and is never deleted
                    self.inuse[overWrite] = pc
                else:
                    self.inuse.append(pc)

            elif sprite.name == "notzigrunt":
                notzigrunt = [\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigrunt.png").convert_alpha(),(144,216)),\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigruntidle2.png").convert_alpha(),(144,216)),\
                    transform.scale(image.load("Assets\\sprites\\npcs\\baddies\\notzigruntdead.png").convert_alpha(),(216,144)),\
                ]
                if overWrite:
                    self.inuse[overWrite] = notzigrunt
                else:
                    self.inuse.append(notzigrunt)
        elif isinstance(sprite, SpriteRemix.Projectile):
            if sprite.name == "pcdefaultproj":
                pcdefaultproj = [\
                    transform.scale(image.load("Assets\\sprites\\projectiles\\pcdefaultproj1.png").convert_alpha(),(108,108)),\
                    transform.scale(image.load("Assets\\sprites\\projectiles\\pcdefaultproj2.png").convert_alpha(),(144,144))\
                ]
                if overWrite:
                    self.inuse[overWrite] = pcdefaultproj
                else:
                    self.inuse.append(pcdefaultproj)
        else:
            self.inuse.append([])


    
