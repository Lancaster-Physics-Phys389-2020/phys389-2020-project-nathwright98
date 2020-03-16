# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 05:18:01 2020

@author: Nathan
"""

import random
import numpy as np
from Particle import Particle

class ComplexParticle(Particle):
    """
    Defines a more complex particle with a decay constant, some predefined decay modes, a variable to determine how long before the particle reaches it's half life, and a boolean to show whether it is stable.
    """
    decayConstant = 0
    decayLife = 0
    decayModes = []
    #Define a variable to track how much time before a half-life is elapsed
    timeRemaining = 0
    stable = False
    accuracy = 0
    
    isotopes = []
    
    def __init__(self, Name, shortName, massNumber, atomicNumber, halfLife, decayModes, stable, accuracy):   
        #Set variables that are present in the base class
        Particle.__init__(self, Name, shortName, massNumber, atomicNumber)
        #Calculate decay constant for the particle based on its half-life
        self.decayConstant = np.log(2)/halfLife
        #Set a decay life variable for the particle based on the accuracy value of the simulation, which is the time it will take for the amount of particles to equal 1/accuracy times the initial amount
        self.decayLife = np.log(accuracy)/self.decayConstant
        self.decayModes = decayModes
        self.timeRemaining = self.decayLife
        self.stable = stable
        self.accuracy = accuracy
        
    def __repr__(self):
        return 'Particle: %s (%s), [N: %s, Z: %s], half-life: %s'%(self.Name, self.shortName, self.massNumber, self.atomicNumber, self.halfLife)
    
    def setTimeRemaining(self, t):
        """
        Functions as a setter method to set the value of 'timeRemaining'.
        """
        #Define a boolean to determine if the particle deacays
        isDecaying = False
        if(t <= 0 and self.stable == False):
            #If a decay life has elapsed, set isDecaying to True
            isDecaying =True
            #Set the time remaining back to the value of the decay life, so that if the particle does not decay it begins counting down again until another half-life has elapsed
            self.timeRemaining = self.decayLife
        else: self.timeRemaining = t
        return isDecaying
        
        
    def checkDecay(self):
        """
        Checks if the particle will decay, and determines the particle to which it will decay.
        """
        #Determine whether a particle will decay based on a random number and the probability of decaying after one decay life
        if(random.random() > 1/self.accuracy):
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
                if(decayMode != None and i.shortName == decayMode.decayProduct):
                    isotope = i
            
            #If a valid isotope has been found, change the variables of this particle such that it takes the properties of the new isotope
            if isotope != None:
                self.Name = isotope.Name
                self.shortName = isotope.shortName
                self.massNumber = isotope.massNumber
                self.atomicNumber = isotope.atomicNumber
                self.decayLife = isotope.decayLife
                self.decayModes = isotope.decayModes
                self.timeRemaining = isotope.decayLife
                self.stable = isotope.stable
                
            if(decayMode != None):
                return decayMode.decayParticles
            else: return None
                    
                
                