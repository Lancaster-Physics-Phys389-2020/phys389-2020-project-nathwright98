# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:10:37 2020

@author: Nathan
"""
import random

class Particle:
    Name = ""
    shortName = ""
    massNumber = 0
    atomicNumber = 0
    halfLife = 0
    decayModes = []
    timeRemaining = 0
    stable = False
    
    isotopes = []
    
    def __init__(self, Name, shortName, massNumber, atomicNumber, halfLife, decayModes, stable):
        self.Name = Name
        self.shortName = shortName
        self.massNumber = massNumber
        self.atomicNumber = atomicNumber
        self.halfLife = halfLife
        self.decayModes = decayModes
        self.timeRemaining = halfLife
        self.stable = stable
        
    def __repr__(self):
        return 'Particle: %s (%s), [N: %s, Z: %s], half-life: %s'%(self.Name, self.shortName, self.massNumber, self.atomicNumber, self.halfLife)
    
    def setTimeRemaining(self, t):
        if(t <= 0):
            self.checkDecay()
            self.timeRemaining = self.halfLife
        else: self.timeRemaining = t
        
    def checkDecay(self):
        if(random.random() > 0.5):
            branchChance = random.random() * 100
            branchCumulative = 0
            branchChanceNeeded = []
            for i in range(len(self.decayModes)):
                branchCumulative += self.decayModes[i].probability
                branchChanceNeeded.append(branchCumulative)
            
            decayMode = None
            for i in range(len(self.decayModes)):
                if branchChance <= branchChanceNeeded[i]:
                    decayMode = self.decayModes[i]
                    break
                else: continue
            
            isotope = None
            for i in self.isotopes:
                #print(decayMode.decayProduct)
                if(i.shortName == decayMode.decayProduct):
                    isotope = i
            
            if isotope != None:
                self.Name = isotope.Name
                self.shortName = isotope.shortName
                self.massNumber = isotope.massNumber
                self.atomicNumber = isotope.atomicNumber
                self.halfLife = isotope.halfLife
                self.decayModes = isotope.decayModes
                self.timeRemaining = isotope.halfLife
                self.stable = isotope.stable
                    
                
                