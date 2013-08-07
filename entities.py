"""
Created on Apr 17, 2012

@author: Erik Bjareholt
"""

from math import radians, sin, cos, hypot, sqrt, pi
import random

import numpy as np
import pygame

import constants


class EntityHandler(dict):
    def __init__(self):
        dict.__init__(self)
    
    def add(self, entity, name=None, debug=False):
        if name is None:
            if entity.name:
                name = entity.name
            else:
                name = random.randint(0, 1000)
                while name in self.keys():
                    name = random.randint(0, 1000)
        else:
            entity.name = name
        self[name] = entity
        if debug:
            print("Added entity #{0} with name: \"{1}\" at pos: {2}".format(str(len(self)), str(name), entity.pos))


class Entity:
    static = True

    def __init__(self, surface=pygame.Surface((10, 10)), pos=np.array((0, 0)), mass=1, name=""):
        self.name = name
        self.surface = surface
        self.pos = pos - np.array((surface.get_width()/2, surface.get_height()/2))
        self.mass = mass

    def __iadd__(self, other):
        self.mass += other.mass
        return self
        
    def draw(self):
        return self.surface

    def getPos(self):
        return self.pos + np.array((self.surface.get_width()/2, self.surface.get_height()/2))


class MovableEntity(Entity):
    static = False

    def __init__(self, force=np.array((0, 0)), *args, **kwargs):
        self.force = force
        Entity.__init__(self, *args, **kwargs)

    def __iadd__(self, other):
        self.force += other.force
        return Entity.__iadd__(self, other)

    def applyAcceleration(self, time):
        self.pos += self.force*time

    def applyForce(self, force):
        self.force += force

    def applyRadForce(self, force, angleRad):
        self.force = force * [cos(angleRad), sin(angleRad)]

    def reverseForce(self):
        self.force = -self.force

        
class Planet(MovableEntity):
    def __init__(self, radius=10, color=(150, 255, 255), *args, **kwargs):
        self.radius = radius
        self.color = color
        self.surface = self.draw()
        MovableEntity.__init__(self, surface=self.surface, *args, **kwargs)
        
    """
    def __iadd__(self, other):
        otherArea = other.radius**2 * pi
        selfArea = self.radius**2 * pi
        self.radius = sqrt((otherArea + selfArea)/pi)
        self.pos = (self.pos[0]-other.radius/2, self.pos[1]-other.radius/2)
        self.surface = self.draw()
        return Entity.__iadd__(self, other)
    """

    def draw(self):
        sideLength = self.radius*2
        surface = pygame.Surface((sideLength, sideLength))
        radiusInt = int(self.radius)
        pygame.draw.circle(surface, self.color, (radiusInt, radiusInt), radiusInt, 0) 
        return surface
