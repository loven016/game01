import pygame
from pygame import sprite
from pygame import font

class CombatText():
    #text: String to render
    #coords: Pair of integer coordinates for the rect
    #duration: Time (ms) to show the combat text
    #fadeInterval: Time interval (ms) between the text floating upwards 1 pixel
    #currentTime: The current time (ms) 
    def __init__(self, text, coords, color, duration, fadeInterval, currentTime):
        self.fadeInterval = fadeInterval
        self.duration = duration
        self.lastAge = currentTime
        textFont = font.Font(None, 100)
        self.surface = textFont.render(text, True, color)
        self.rect = self.surface.get_rect()
        self.rect.center = coords
        
    #increment the animation by one frame.
    #return true if the text still needs to be rendered, false if it has completed the animation.
    #currentTime: The current time (ms)
    def progress(self, currentTime):
        if self.duration > 0:
            timeDiff = currentTime - self.lastAge
            if timeDiff > self.fadeInterval:
                self.duration = self.duration - timeDiff
                self.lastAge = currentTime
                if self.rect.center[1] > 0:
                    self.rect.center = (self.rect.center[0], self.rect.center[1] - 1)
            return True
        else:
            return False
        
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        