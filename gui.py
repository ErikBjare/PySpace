'''
Created on May 18, 2012

@author: Erik Bjareholt
'''

import pygame

pygame.font.init()
standardFont = pygame.font.Font("fonts/freesansbold.ttf", 24)


class Activity:
    def __init__(self, size):
        self.widgets = []
        self.size = size
        
class HUD(Activity):
    def __init__(self, size):
        Activity.__init__(self, size)
        self.fpsCounter = FPSCounter((10,10))
        
    def draw(self, FPS):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        surPos = self.fpsCounter.draw(FPS)
        self.surface.blit(surPos[0], surPos[1])
        return self.surface


class Widget:
    def setPos(self, pos):
        self.pos = pos

class FPSCounter(Widget):
    def __init__(self, pos):
        self.setPos(pos)
    
    def draw(self, FPS):
        FPS = str(FPS).split(".")[0]
        return (standardFont.render(FPS, True, (255,255,0)), self.pos)
