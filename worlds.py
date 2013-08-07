"""
Created on May 15, 2012

@author: Erik Bjareholt
"""

from math import sqrt

import pygame
import numpy as np

import entities

screenSize = (512, 512)

class World(list):
    def __init__(self, name, timeMult, background):
        self.name = name
        self.timeMult = timeMult
        self.background = background
        list.__init__(self)

worlds = []

if False:
    #---------------------------------------
    # An empty solar system, consisting of only one sun.
    #---------------------------------------

    emptySystem = World("Empty", 10**7, pygame.Surface(screenSize))

    sun = entities.Planet(pos=np.array((0, 0)), force=np.array((10, 10)), color=pygame.Color("orange"), name="Sun")
    emptySystem.append(sun)

    worlds.append(emptySystem)

if True:
    #---------------------------------------
    # Basic orbit test
    #---------------------------------------

    background = pygame.Surface(screenSize)
    pygame.draw.circle(background, (255, 0, 255), (screenSize[0]/2, screenSize[1]/2), 200, 1)
    testS = World("testS", 10**7, background=background)

    sun = entities.Planet(mass=10, radius=10, color=pygame.Color("orange"), name="Sun")
    earth = entities.Planet(pos=np.array((0, -200)), radius=3, mass=1, force=np.array((0.0000182619823677*sqrt(2), 0)), name="Earth")
    #                                       1,8261982367749674289465871228867e-6
    testS.append(sun)
    testS.append(earth)

    worlds.append(testS)


if False:
    #---------------------------------------
    # Lagrangian Point Test
    #---------------------------------------


    testLagPoint = World(10**7, pygame.Surface(screenSize))

    sun = entities.Planet((0,0), 10, 10, color=pygame.Color("orange"), static=True, name="Sun")
    earth = entities.Planet((0,-200), 1, 3, static=True, name="Earth")
    testLagPoint.append(sun)
    testLagPoint.append(earth)

    worlds.append(testLagPoint)


if False:
    #---------------------------------------
    # Basic orbit test
    #---------------------------------------

    background = pygame.Surface(screenSize)
    pygame.draw.circle(background, (255,0,255), (screenSize[0]/2, screenSize[1]/2), 200, 1)
    moonSystem = World(10**3, background=background)

    earth = entities.Planet((0,0), 59.7**24, 10, static=True, color=pygame.Color("orange"), name="Earth")
    moon = entities.Planet((0,38), 7.35**20, 3, Fx=1.023*sqrt(2), Fy=0, name="Moon")
    # 1,8261982367749674289465871228867e-6
    moonSystem.append(earth)
    moonSystem.append(moon)

    worlds.append(moonSystem)

"""
    In this world we try out Astrodynamics.
                
    The first formula is for a circular orbit.
                
    The formulas can be found at: 
     - http://en.wikipedia.org/wiki/Astrodynamics
     - http://en.wikipedia.org/wiki/Escape_orbit
"""