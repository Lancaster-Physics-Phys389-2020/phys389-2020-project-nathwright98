# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:10:37 2020

@author: Nathan
"""
import random

class Particle:
    """
    Defines a particle with a name, a short name (to function as a simple identifier), a mass number and atomic number, a half life, some predefined decay modes, a variable to determine how long before the particle reaches it's half life, and a boolean to show whether it is stable.
    """
    Name = ""
    shortName = ""
    massNumber = 0
    atomicNumber = 0
    halfLife = 0
    decayModes = []
    #Define a variable to track how much time before a half-life is elapsed
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
        """
        Functions as a setter method to set the value of 'timeRemaining'.
        """
        if(t <= 0):
            #If a half-life has elapsed, check if the particle will decay
            self.checkDecay()
            #Set the time remaining back to the value of the half-life, so that if the particle does not decay it begins counting down again until another half-life has elapsed
            self.timeRemaining = self.halfLife
        else: self.timeRemaining = t
        
    def checkDecay(self):
        """
        Checks if the particle will decay, and determines the particle to which it will decay.
        """
        #50% chance for particle to decay after each half-life
        if(random.random() > 0.5):
            #Generate a random float between 0 and 100 which will determine the branch that is taken
            branchChance = random.random() * 100
            branchCumulative = 0
            branchChanceNeeded = []
            #Add all the branching fractions as percentages such that they sum to 100, and determine a range from 0-100 which the branching fraction corresponds to as a percentage chance
            for i in range(len(self.decayModes)):
                branchCumulative += self.decayModes[i].probability
                branchChanceNeeded.append(branchCumulative)
            
            decayMode = None
            for i in range(len(self.decayModes)):
                #If the random float is within the range that the given decay mode occupies between 0 and 100, pick that mode
                if branchChance <= branchChanceNeeded[i]:
                    decayMode = self.decayModes[i]
                    break
                else: continue
            
            isotope = None
            for i in self.isotopes:
                #Find the particle in the 'isotopes' list with an ID matching that of the decay particle defined in the decay mode
                if(i.shortName == decayMode.decayProduct):
                    isotope = i
            
            #If a valid isotope has been found, change the variables of this particle such that it takes the properties of the new isotope
            if isotope != None:
                self.Name = isotope.Name
                self.shortName = isotope.shortName
                self.massNumber = isotope.massNumber
                self.atomicNumber = isotope.atomicNumber
                self.halfLife = isotope.halfLife
                self.decayModes = isotope.decayModes
                self.timeRemaining = isotope.halfLife
                self.stable = isotope.stable
                    
                
                