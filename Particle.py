# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:10:37 2020

@author: Nathan
"""

class Particle:
    """
    Defines a particle with a name, a short name (to function as a simple identifier), a mass number and an atomic number
    """
    Name = ""
    shortName = ""
    massNumber = 0
    atomicNumber = 0
    
    def __init__(self, Name, shortName, massNumber, atomicNumber):
        self.Name = Name
        self.shortName = shortName
        self.massNumber = massNumber
        self.atomicNumber = atomicNumber
        
    def __repr__(self):
        return 'Particle: %s (%s), [N: %s, Z: %s]'%(self.Name, self.shortName, self.massNumber, self.atomicNumber)