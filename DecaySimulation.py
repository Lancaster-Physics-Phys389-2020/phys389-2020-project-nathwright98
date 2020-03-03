# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:33:11 2020

@author: Nathan
"""
from Particle import Particle
from DecayMode import DecayMode
import csv
import ast
import copy
import matplotlib.pyplot as plt
import os

class DecaySimulation:
    
    simulationName = "Simulation"
    time = 0
    step = 0
    
    particleData = []
    times = []
    steps = []
    
    isotopes = []
    particles = []

    def __init__(self):
        self.initialiseIsotopes()
        
        for i in range(10000):
            self.particles.append(copy.copy(self.isotopes[0]))
            self.particles[i].isotopes = self.isotopes
        
        self.simulate()
        
    def __repr__(self):
        return "Decay Simulation"
    
    def initialiseIsotopes(self):
        with open('isotopeData.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter = ',')
            lineCount = 0

            for row in csvReader:
                if lineCount > 0:
                    decayModes = []
                    stable = False
                    if(row[4] != "stable"):
                        for x in row[5].split("&", 1):
                            x = x.strip("[]")
                            dm = x.split(",", 2)
                            decayModes.append(DecayMode(dm[0],dm[1],ast.literal_eval(dm[2])))
                    else: stable = True
                    self.isotopes.append(Particle(row[0],row[1],eval(row[2]),eval(row[3]),eval(row[4]),decayModes,stable))
                    self.particleData.append([])
                lineCount += 1
                
    def findLowestHalfLife(self):
        tempParticles = []
        for p in self.particles:
            if p.stable != True:
                tempParticles.append(p)
        return float(min(i.halfLife for i in tempParticles))
    
    def checkIfComplete(self):
        if(any(i.stable == False for i in self.particles)):
            return False
        else: return True
    
    def simulate(self):
        self.addData()
        while(self.checkIfComplete() == False):
            self.timestep()
            
        self.plotData()
            
    def timestep(self):
        timeToSimulate = self.findLowestHalfLife()
        self.time += timeToSimulate
        self.step += 1
        for p in self.particles:
            if(p.stable != True):
                p.setTimeRemaining(p.timeRemaining - timeToSimulate)
        self.addData()
    
    def addData(self):
        self.times.append(self.time)
        self.steps.append(self.step)
        for i in range(len(self.isotopes)):
            pNames = list(p.shortName for p in self.particles)
            iCount = pNames.count(self.isotopes[i].shortName)
            self.particleData[i].append(iCount)
            
    def plotData(self):
        try:
            os.mkdir(self.simulationName)
        except:
            pass
        
        plt.stackplot(self.times, self.particleData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('t /s')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes over time")
        plt.plot()
        try:
            plt.savefig(self.simulationName + "/time.png")
        except:
            plt.savefig(self.simulationName + "_time.png")
        plt.show()
            
        plt.stackplot(self.steps, self.particleData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('steps')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes per step")
        plt.plot()
        try:
            plt.savefig(self.simulationName + "/steps.png")
        except:
            plt.savefig(self.simulationName + "_steps.png")
        plt.show()
            
        for i in range(len(self.isotopes)):
            iName = self.isotopes[i].shortName
            plt.plot(self.times, self.particleData[i], "k-", label = iName)
            plt.xlabel('t /s')
            plt.ylabel('N')
            plt.legend()
            plt.title("Population of " + iName + " over time")
            plt.plot()
            try:
                plt.savefig(self.simulationName + "/" + iName + ".png")
            except:
                plt.savefig(self.simulationName + "_" + iName + ".png")
            plt.show()
        
        