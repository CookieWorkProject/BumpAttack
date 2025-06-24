import pygame

from objects.BasicObject import BasicObject
from objects.Coin import Coin
from objects.Enemy import Enemy
from util.Controller import Controller
import numpy
class Player(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        self.controller = Controller(False,False,False,False)
        self.hp = 10
        self.knockback = 0
        self.knockbackX = 0
        self.knockbackY = 0
        self.knockbackPower = 0
    def step(self):
        if self.knockback>0:
            self.rect.left+=self.knockbackX*self.knockbackPower
            self.rect.top+=self.knockbackY*self.knockbackPower
            self.knockback-=1
            #stun eeffect
            if self.knockback<10:
                self.knockbackPower = 0
        else:
            if self.controller.right:
                self.rect.left+=1
            if self.controller.left:
                self.rect.left-=1
            if self.controller.up:
                self.rect.top-=1
            if self.controller.down:
                self.rect.top+=1
    def draw(self,surface):
        pygame.draw.ellipse(surface, (0, 255, 0), self.rect)
    def collision(self,gameObjects):
        for a in gameObjects:
            if a.active == False or self.rect.colliderect(a) == False:
                continue
            if type(a) == Coin:
                a.active = False
                
            elif type(a) == Enemy:
                x = a.getCenterX()-self.getCenterX()
                y = a.getCenterY()-self.getCenterY()
                angle = abs(self.angle_between_vectors_degrees(self.controller.getMovementVectors(),(x,y)))
                print(angle)
                if angle <15:
                    self.setKnockback(30,-numpy.sign(x),-numpy.sign(y),3)
                    self.hp -=2
                elif angle <30:
                    self.setKnockback(20,-numpy.sign(x),-numpy.sign(y),2)
                    self.hp -=1
                    a.active = False
                else:
                    a.active = False
                if self.hp <=0:
                    self.active = False
    def setKnockback(self,frames,x,y,power):
        self.knockback = frames
        self.knockbackX = x
        self.knockbackY = y
        self.knockbackPower = power