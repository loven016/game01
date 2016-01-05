import pygame
from pygame import *
import SpriteRemix
import Character

class Animation():
    def __init__(self):
        self.inuse = [] #list of lists of images belonging to a sprite
        self.count = -1 #cardinality of inuse (first added element must have 0th index)
    def animate(self, spritesList, now):

        for j in range(len(spritesList)):
                
            for i in range(len(spritesList[j])):
                if isinstance(spritesList[j][i], Character.PlayerCharacterSprite):
                    tempLoc = spritesList[j][i].rect.bottomleft
                    if spritesList[j][i].name == "pc":

                        if spritesList[j][i].state["idle"]:
                            if now % 1500 > 750:                    
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])
                            elif now % 1500 > 400 or now % 1500 <= 150:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][1])
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][2])

                        elif spritesList[j][i].state["jumping"]:
                            if spritesList[j][i].state["shooting"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["shooting"] = False
                                    
                            elif spritesList[j][i].state["attacking"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["attacking"] = False

                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][5])

                        elif spritesList[j][i].state["falling"]:
                            if spritesList[j][i].state["shooting"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["shooting"] = False
                                    
                            elif spritesList[j][i].state["attacking"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["attacking"] = False
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][6])
                            
                        elif spritesList[j][i].state["running"]:
                            if spritesList[j][i].state["shooting"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["shooting"] = False
                                    
                            elif spritesList[j][i].state["attacking"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["attacking"] = False
                                    
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][3])

                        elif spritesList[j][i].state["ducking"]:
                            #print("ducking")
                            if spritesList[j][i].state["shooting"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][7])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["shooting"] = False
                                    
                            elif spritesList[j][i].state["attacking"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][7])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["attacking"] = False
                                    
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][7])

                                                
                        elif spritesList[j][i].state["ready"]:
                            #print("ready")
                            if spritesList[j][i].state["shooting"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["shooting"] = False
                                    
                            elif spritesList[j][i].state["attacking"]:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][4])
                                if now - spritesList[j][i].last["meleed"] > 300:
                                    spritesList[j][i].state["attacking"] = False
                                    
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][3])

                        #TODO: all frames
                        elif spritesList[j][i].state["dying"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])

                        #TODO: frame
                        elif spritesList[j][i].state["dead"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])

                    if spritesList[j][i].xflip:
                        spritesList[j][i].setImage(transform.flip(spritesList[j][i].image, True, False))
                            
                    spritesList[j][i].rect.bottomleft = tempLoc
                    
                elif isinstance(spritesList[j][i], SpriteRemix.Weapon):

                    tempLoc = spritesList[j][i].rect.bottomleft
                    
                    if spritesList[j][i].name == "weapon":

                        spritesList[j][i].visible = True
                        
                        if spritesList[j][i].state["dying"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])

                        elif spritesList[j][i].state["attacking"] or spritesList[j][i].state["shooting"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][1])

                        elif spritesList[j][i].state["jumping"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])

                        elif spritesList[j][i].state["falling"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])

                        elif spritesList[j][i].state["running"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])
                            
                        elif spritesList[j][i].state["ready"]:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])
                            #this doesn't work, and I don't know why. Altering value instead of object perhaps?
                            '''spritesList[j][i].rect.midright = spritesList[0][0].rect.midleft'''

                        if spritesList[j][i].state["idle"] or spritesList[j][i].state["dead"] or spritesList[j][i].state["ducking"]:
                            spritesList[j][i].visible = False

                    if spritesList[j][i].xflip:
                        spritesList[j][i].setImage(transform.flip(spritesList[j][i].image, True, False))
                    
                    spritesList[j][i].rect.bottomleft = tempLoc

                elif isinstance(spritesList[j][i], Character.EnemyCharacterSprite):

                    tempLoc = spritesList[j][i].rect.bottomleft
                    
                    if spritesList[j][i].name == "notzigrunt":
                        if spritesList[j][i].stateVal == 0:
                            if now % 1500 < 250:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][1])
                            else:
                                spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])
                                
                        else:
                            spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][2])

                    if spritesList[j][i].xflip:
                        spritesList[j][i].setImage(transform.flip(spritesList[j][i].image, True, False))

                    spritesList[j][i].rect.bottomleft = tempLoc

                elif isinstance(spritesList[j][i], SpriteRemix.Projectile):
                    tempLoc = spritesList[j][i].rect.center
                    if spritesList[j][i].stateVal == 1:
                        tempImage = transform.rotate(self.inuse[spritesList[j][i].id][0],-90)
                        self.inuse[spritesList[j][i].id][0] = self.inuse[spritesList[j][i].id][1]
                        self.inuse[spritesList[j][i].id][1] = tempImage
                        spritesList[j][i].setImage(self.inuse[spritesList[j][i].id][0])
                    spritesList[j][i].rect.center = tempLoc

                elif isinstance(spritesList[j][i], SpriteRemix.Background):
                    if spritesList[j][i].stateVal == 1:
                        if now - spritesList[j][i].lastUpdate > 16:
                            spritesList[j][i].lastUpdate = now
                            spritesList[j][i].velocity = [2,0]
                        else:
                            spritesList[j][i].velocity = [0,0]
                        if spritesList[j][i].rect.left >= 1920:
                            spritesList[j][i].rect.right = 0

                                             
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
        
        if isinstance(sprite, Character.PlayerCharacterSprite):
            if sprite.name == "pc":
                pc = [\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle1.png").convert_alpha(),(144,216)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle2.png").convert_alpha(),(144,219)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcidle3.png").convert_alpha(),(144,221)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcready1.png").convert_alpha(),(94,209)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcattack4.png").convert_alpha(),(152,207)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcjump1.png").convert_alpha(),(128,202)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcfall1.png").convert_alpha(),(106,197)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pccrouch1.png").convert_alpha(),(99,111))\
                ]
                if overWrite: #0 is PC and is never deleted
                    self.inuse[overWrite] = pc
                else:
                    self.inuse.append(pc)

        elif isinstance(sprite, SpriteRemix.Weapon):
            if sprite.name == "weapon":
                pcweapon = [\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcreadyscythe1.png").convert_alpha(),(84,92)),\
                    transform.scale(image.load("Assets\\sprites\\pc\\pcattackscythe4.png").convert_alpha(),(80,70))\
                ]
                if overWrite:
                    self.inuse[overWrite] = pcweapon
                else:
                    self.inuse.append(pcweapon)

        elif isinstance(sprite, Character.EnemyCharacterSprite):
            if sprite.name == "notzigrunt":
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



