'''
Created on Apr 17, 2012

@author: Erik Bjareholt
'''

from math import radians, sin, cos, hypot, sqrt, pi
import random

import pygame

import constants

class EntityHandler:
    def __init__(self):
        self.entities = {}
    
    def add(self, entity, name="", debug=False):
        if name=="":
            if entity.name:
                name = entity.name
            else:
                name = random.randint(0, 1000)
                while name in self.entities.keys():
                    name = random.randint(0, 1000)
        else:
            entity.name = name
        self.entities[name] = entity
        if debug:
            print("Added entity #{0} with name: \"{1}\" at pos: {2}".format(str(len(self.entities)), str(name), entity.pos))

    def __delitem__(self, name):
        del self.entities[name]

    def __getitem__(self, key):
        return self.entities[key]
    
    def __setitem__(self, key, value):
        self.entities[key] = value

    def __len__(self):
        return len(self.entities)


class Entity:
    def __init__(self, Surface, pos, mass, Fx=0, Fy=0, static=False, name=""):
        self.name = name
        self.surface = Surface
        self.pos = pos
        self.mass = mass
        self.Fx = Fx
        self.Fy = Fy
        self.static = static
        
    def __iadd__(self, other):
        self.mass += other.mass
        self.Fx += other.Fx
        self.Fy += other.Fy
        return self
        
    def draw(self):
        return self.surface
    
    def applyAcceleration(self, time):
        if not self.static:
            self.pos = (self.pos[0]+(self.Fx*time), self.pos[1]+(self.Fy*time))
        
    def applyForce(self, Fx, Fy):
        if not self.static:
            self.Fx += Fx
            self.Fy += Fy
        
    def applyRadForce(self, force, angleRad):
        if not self.static:
            self.Fx = force * cos(angleRad)
            self.Fy = force * sin(angleRad)
        
    def applyGravity(self, affectorMass, distance, cyclesPerSec, debug=False):
        if not self.static:
            Fx = constants.G * ((self.mass*affectorMass)/distance[0]**2) * distance[1] * cyclesPerSec
            Fy = constants.G * ((self.mass*affectorMass)/distance[0]**2) * distance[2] * cyclesPerSec
            self.Fx += Fx
            self.Fy += Fy
            if debug:
                print("New pos {0}\nAcceleration: {1},{2}\nRadius: {3}".format(self.pos, self.Fx, self.Fy, distance))
            return (Fx, Fy)
    
    
    def getPosition(self):
        return [self.pos[0], self.pos[1]]

    def getCenter(self):
        return [self.pos[0] + self.surface.get_width()/2, self.pos[1] + self.surface.get_height()/2]
    
    def reverseForce(self):
        self.Fx = -self.Fx
        self.Fy = -self.Fy
        
        
class Planet(Entity):
    def __init__(self, pos, mass, radius, Fx=0, Fy=0, static=False, color=(150,255,255), name=""):
        self.radius = radius
        self.color = color
        self.surface = self.draw()
        Entity.__init__(self, self.surface, (pos[0]-radius, pos[1]-radius), mass, Fx, Fy, static, name)
        
    def __iadd__(self, other):
        otherArea = other.radius**2 * pi
        selfArea = self.radius**2 * pi
        self.radius = sqrt((otherArea + selfArea)/pi)
        self.pos = (self.pos[0]-other.radius/2, self.pos[1]-other.radius/2)
        self.surface = self.draw()
        return Entity.__iadd__(self, other)
        
    def draw(self):
        sideLength = self.radius*2
        surface = pygame.Surface((sideLength, sideLength))
        radiusInt = int(self.radius)
        pygame.draw.circle(surface, self.color, (radiusInt, radiusInt), radiusInt, 0) 
        return surface
