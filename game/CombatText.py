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
        self.textFont = font.Font(None, 100)
        self.text = text
        self.surface = self.textFont.render(text, True, color)
        self.finalSurf = self.surface
        self.alpha = 255
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
                #NOTE: as far as I can tell, this shit doesn't fucking work. Feel free to fuck around with it.
                '''self.finalSurf = pygame.Surface((self.rect.width,self.rect.height))
                self.alpha -= 6
                self.finalSurf.set_alpha(self.alpha)'''
            return True
        else:
            return False
        
    def draw(self, screen):
        '''self.finalSurf.blit(self.surface, (0,0))
        screen.blit(self.finalSurf, self.rect)'''
        screen.blit(self.surface, self.rect)
        
