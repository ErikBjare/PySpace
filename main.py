'''
Created on Apr 17, 2012

@author: Erik Bjareholt
'''

from math import sqrt
import re
import platform

import pygame
from pygame.locals import *

import worlds
import entities
import gui


class Main:
    def __init__(self):
        self.running = True
        pygame.display.init()
        pygame.display.set_caption('PySpace')
        pygame.display.set_icon(pygame.image.load("./icon.gif"))
    
        while self.running:
            handle()
            screen = engine.render()
            pygame.display.flip()
        
        
class Engine:
    def __init__(self):
        print("Hello, master. Gravity and Acceleration Logitizer 9000 at your service.\n" + 
              "Name: GAL9000 | Health: I'm great thank you.\n" +
              "Python Version: " + platform.python_version() + " | PyGame Version: " + pygame.ver)
        while True:
            answer = raw_input("\nPick a resolution:\n" +
                               "1 - 512*512*32\n" +
                               "2 - 1024*1024*32\n" +
                               "3 - 1680*1050*32 Fullscreen\n" +
                               "Choice: ")
            if answer == "1":
                self.mode = [(512,512), 0, 32]
                break
            if answer == "2":
                self.mode = [(1024,1024), 0, 32]
                break
            if answer == "3":
                self.mode = [(1680,1050), pygame.FULLSCREEN, 32]
                break
        self.screen = pygame.display.set_mode(self.mode[0], self.mode[1], self.mode[2])
        self.activity = gui.HUD(self.mode[0])
        self.fpsLimit = 10000
        
        self.background = pygame.Surface(self.mode[0])
        self.background.fill((0,0,0))
        
        self.clock = pygame.time.Clock()
        self.drawGUI()
        
        self.entities = entities.EntityHandler()
        self.load()
        
        self.cycleInterval = 15 # Time between physics cycles, in ms.
        
        pygame.time.set_timer(pygame.USEREVENT + 1, self.cycleInterval)
        pygame.time.set_timer(pygame.USEREVENT + 2, 250)
        
        self.waitForInput = False    
    
    def render(self):
        if self.waitForInput:
            self.command()
        self.screen.blit(self.background, (0,0))
        for entityKey in self.entities.entities.keys():
            # pos = self.entities[entityKey].getPosition()
            pos = self.entities[entityKey].getPosition()
            pos[0] = pos[0] + (self.mode[0][0]/2)
            pos[1] = pos[1] + (self.mode[0][1]/2)
            self.screen.blit(self.entities[entityKey].surface, pos)
        self.renderGUI()
        self.clock.tick(self.fpsLimit)
        return self.screen
    
    def renderGUI(self):
        self.screen.blit(self.gui, (0,0))
    
    def drawGUI(self):
        self.gui = self.activity.draw(self.clock.get_fps())
    
    def command(self, cmd=None):
        if not cmd:
            cmd = raw_input("# ")
        if cmd == "help":
            print("Commands available:\nUNDER CODESTRUCTION")
            #for command in commands:
            #    print("{0} - {1} (ID: {2}".format(command[1], command[2], command[0]))
        elif cmd == "add":
            name = raw_input("Name: ")
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            Fx = float(raw_input("Fx: "))
            Fy = float(raw_input("Fy: "))
            radius = int(raw_input("Radius: "))
            mass = int(raw_input("Mass: "))
            self.entities.add(entities.Planet((x, y), mass, radius, Fx, Fy), name=name, debug=True)
        elif cmd == "delete":
            name = raw_input("Delete (name): ")
            del self.entities[name]
        elif cmd == "clear":
            """
                Clears the world of all entities.
                
                Planned:
                    Clears entities matching a criteria.
            """
            for entityKey in self.entities.entities.keys():
                del self.entities[entityKey]
            print("Cleared world of all entities!")
            
        elif cmd == "list":
            """
                Prints a list of all entities in the world
                
                Planned: 
                    Print a list of entities matching a criteria.
                    Search for entities by name, radius, mass etc.
                    Sort the list by name, radius, mass etc.
                    Possibility to choose level of data with a parameter.
            """
            for entityKey in self.entities.entities.keys():
                className = self.entities[entityKey].__class__.__name__
                print("Name: {0}, Type: {1}, Weight: {2}\nPosition: {3}\nForce: ({4}, {5})".format(entityKey, className, self.entities[entityKey].mass, 
                                                                                 self.entities[entityKey].pos,
                                                                                 self.entities[entityKey].Fx, self.entities[entityKey].Fy))
                if className == "Planet":
                    print("Radius: {2}".format(entityKey, self.entities[entityKey].mass, self.entities[entityKey].radius))
                print("")    
                
        elif cmd == "load":
            """
                Opens up the load world dialog.
            """
            self.load()
        
        elif cmd == "get":
            """
                Can be used to get certain data.
            """
            cmd = raw_input("Get: ")
            if cmd == "fps":
                print("Last FPS: {0}".format(self.fps))
        
        elif cmd == "set":
            """
                Can be used to set certain data.
            """
            cmd = raw_input("Set: ")
            if cmd == "fpsLimit":
                self.fpsLimit = int(raw_input("FPS Limit: "))
                
        elif cmd == "eval":
            """
                Runs eval() on input and prints result.
            """
            result = input("eval():")
            print(result)
            
        elif re.match(r"^time.set$", cmd):
            """
                Sets cycleTime
                
                Planned:
                    Takes cycleTime as an argument, therefore
                    the re.match(...) in the elif statement.
            """
            newTime = int(input("Enter expression to eval(): "))
            self.cycleTime = newTime
            
        elif cmd == "end":
            print("Command mode ended")
            self.waitForInput = False
            
        elif cmd == "quit" or cmd == "exit":
            main.running = False
            
        else:
            print("Unknown command, for a list write \"help\" or read the documentation.")
    
    def physicsCycle(self):
        """
            This is a very complex function where a lot can go wrong
            and cause non-natural results. Currently a lot does, so
            put some work into the proper way of writing it to obtain
            a far higher degree of accuracy.
        """
        self.deletionQue = []
        timePerSec = self.timeMult*self.cycleInterval/1000
        for entityKey in self.entities.entities.keys():
            self.entities[entityKey].applyAcceleration(timePerSec)
            for affectorKey in self.entities.entities.keys():
                if entityKey != affectorKey:
                    entityPos = self.entities[entityKey].getCenter()
                    affectorPos = self.entities[affectorKey].getCenter()
                    dX = affectorPos[0] - entityPos[0]
                    dY = affectorPos[1] - entityPos[1]
                    distance = sqrt((dX**2) + (dY**2))
                    radius = self.entities[entityKey].radius + self.entities[affectorKey].radius
                    
                    collision = self.sphereCollision(radius, distance, entityKey, affectorKey)
                    if not collision:
                        force = self.entities[entityKey].applyGravity(self.entities[affectorKey].mass, (distance, dX, dY), timePerSec)
                        if force:
                            self.entities[affectorKey].applyForce(-force[0]/timePerSec, -force[1]/timePerSec)
            
        for key in self.deletionQue:
            del self.entities[key]
    
    def sphereCollision(self, radius, distance, entityKey, affectorKey):
        if radius > distance:
            if entityKey not in self.deletionQue and affectorKey not in self.deletionQue:
                if self.entities[entityKey].mass > self.entities[affectorKey].mass:
                    keepKey = entityKey
                    deleteKey = affectorKey
                else:
                    keepKey = affectorKey
                    deleteKey = entityKey
                self.entities[keepKey] += self.entities[deleteKey]
                self.deletionQue.append(deleteKey)
            return True
        return False
    
    def load(self, loadWorld=None):
        if not loadWorld:
            print("\nAvailable worlds")
            listNo = 1
            for worldKey in worlds.worlds.keys():
                print("{0} - {1}".format(listNo, worldKey))
                listNo += 1
            loadWorld = raw_input("World: ")
            self.command("clear")
        try:
            loadWorld = worlds.worlds[worlds.worlds.keys()[int(loadWorld)-1]]
        except:
            if loadWorld in worlds.worlds.keys():
                loadWorld = worlds.worlds[loadWorld]
            else:
                print("World {0} could not be found. None loaded.".format(loadWorld))
                self.timeMult = 10**7
                loadWorld = None
    
        if loadWorld:
            self.timeMult = loadWorld.timeMult
            for entity in loadWorld:
                self.entities.add(entity, name=entity.name)
            self.background.blit(loadWorld.background, (self.mode[0][0]/2-loadWorld.background.get_width()/2,
                                                        self.mode[0][1]/2-loadWorld.background.get_height()/2))

def handle():
    #Event handler
    for event in pygame.event.get():
        if event.type == USEREVENT + 1:
            engine.physicsCycle()
        elif event.type == USEREVENT + 2:
            engine.drawGUI()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                pass
            elif event.key == K_LEFT:
                engine.cycleTime = -engine.cycleTime
            elif event.key == K_i:
                print("Command mode entered!")
                engine.waitForInput = True
            elif event.key == K_ESCAPE:
                main.running = False
        elif event.type == MOUSEBUTTONDOWN:
            worldPos = (event.pos[0]-engine.mode[0][0]/2, event.pos[1]-engine.mode[0][1]/2)
            if event.button == 1:
                engine.entities.add(entities.Planet(worldPos, 1, 1), debug=True)
            elif event.button == 3:
                print("Mousebutton 3 clicked the world at: {0}".format(worldPos))
        elif event.type == QUIT:
            main.running = False
    
    #Input handler
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        pass

if __name__ == '__main__':
    engine = Engine()
    main = Main()
