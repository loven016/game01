import sys
import pygame
from pygame import *
from VectorMath import *

class Movement():
    def accel(char, vel):
        char.velocity[0] = min(max(char.velocity[0]+vel, -24), 24)
        
    def coast(char, xvel, yvel = 0):
        char.xcoast += xvel
        char.ycoast += yvel

    def jump(char):
        #char.falling = True
        if char.numJumps == 2:
            char.velocity[1] -= 40
            char.numJumps -= 1
        elif char.numJumps == 1:
            char.velocity[1] = -30
            char.numJumps -= 1

    #calculates the velocity of a projectile at instantiation
    def shoot(proj):
        direction = [proj.dest[0]-proj.origin[0], proj.dest[1]-proj.origin[1]]
        unitvec = VectorMath.normalize(direction)
        return VectorMath.mult(unitvec,proj.speed)
        
