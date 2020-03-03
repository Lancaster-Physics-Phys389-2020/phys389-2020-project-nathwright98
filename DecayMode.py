# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:19:20 2020

@author: Nathan
"""

class DecayMode:
    decayProduct = ""
    decayParticle = None
    probability = 0
    
    def __init__(self, decayProduct, decayParticle, probability):
        self.decayProduct = decayProduct
        self.decayParticle = decayParticle
        self.probability = probability
        
    def __repr__(self):
        return 'Decay to %s with decay particle %s and probability %s'%(self.decayProduct, self.decayParticle, self.probability)
