import pygame
from pygame import *
from SpriteRemix import Tile

#NOTE: This is very much in progress, do not import into main until ready to test.
#TODO: We need a Map() class that stores all the tiles lists and has methods
#to move the pc between rooms
class Room():
    def __init__(pcentry, bg, tileset, tiles, enemies) #eventually will include pickups and doodads
        #tiles to be passed as list of lists (16x32) of strings of file names
        #tileset will be a string representing the dir that the tiles are held in
                 
        self.tileDir = "Assets\\sprites\\tiles\\"+tileset+"\\"
        for i in range(16):
            for j in range(32):
                tempTilePath = self.tileDir+tiles[i][j]
                tempTile = SpriteRemix.Tile(transform.scale(image.load(tempTilePath).convert(),(60,60)))
                tempTile.rect.topleft = (i*60,j*60)
                screen.blit(tempTile.image, tempTile.rect)
