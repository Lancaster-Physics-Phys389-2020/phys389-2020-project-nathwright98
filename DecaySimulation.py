# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:33:11 2020

@author: Nathan
"""
#from Particle import Particle
#from DecayMode import DecayMode
#import csv
#import ast
#import copy
import matplotlib.pyplot as plt
import os

class DecaySimulation:
    """
    Defines a simulation with given parameters which will then simulate the decay of a number of particles, at a given level of accuracy, continuing until all remaining particles are stable.
    """
    simulationName = "Simulation"
    time = 0
    step = 0
    N = 0
    accuracy = 0
    
    particleData = []
    times = []
    steps = []
    
    isotopes = []
    particles = []

    def __init__(self, name, N, accuracy, isotopes, particles):
        #Clear all remaining variables in case this class is called more than once.
        self.clearVariables()
        
        self.N = N
        self.accuracy = accuracy
        
        #Allow this class to access the list of isotopes
        self.isotopes = isotopes
        #For each isotope, add an empty list to the particleData list
        for i in isotopes:
            self.particleData.append([])
        #Define the list of particles that the simulation will use, based on the list that is passed to this class
        self.particles = particles
        #Start the simulation
        self.simulate()
        
    def __repr__(self):
        return "Decay Simulation"
                
    def findLowestRemaining(self):
        """
        Finds the particle in the list with the lowest remaining time, then returns this value.
        """
        tempParticles = []
        for p in self.particles:
            #Exclude stable particles as they have no decay life value
            if p.stable != True:
                tempParticles.append(p)
        return float(min(i.timeRemaining for i in tempParticles))
    
    def checkIfComplete(self):
        """
        Checks if the simulation is complete by checking if all the particles are stable.
        """
        if(any(i.stable == False for i in self.particles)):
            return False
        else: return True
    
    def simulate(self):
        """
        Runs the simulation until all the particles are stable.
        """
        #Record data before the first step of the simulation takes place
        self.addData()
        #While there are still unstable particles, continue simulating time steps
        while(self.checkIfComplete() == False):
            #Simulate one time step
            self.timestep()
        
        #Plot all data
        self.plotData()
            
    def timestep(self):
        """
        Simulates one time step, in which all particles have their remaining time variable decremented by an amount of time equal to the lowest half life.
        """
        #Determine the time to simulate by calling a function to return the lowest half time
        timeToSimulate = self.findLowestRemaining()
        #Add the simulated time to a total time variable
        self.time += timeToSimulate
        #Increment the step variable by one so that the number of steps in the simulation can be counted
        self.step += 1
        for p in self.particles:
            if(p.stable != True):
                #Decrement the timeRemaining variable of the particle
                p.setTimeRemaining(p.timeRemaining - timeToSimulate)
        #At the end of the time-step, record data about the simulation
        self.addData()
    
    def addData(self):
        """
        Records data about all the particles in the simulation, as well as the corresponding time value and step value.
        """
        self.times.append(self.time)
        self.steps.append(self.step)
        for i in range(len(self.isotopes)):
            #Record a list of names of isotopes to be used in the legend
            pNames = list(p.shortName for p in self.particles)
            #Record how many of each isotope are present in the list of particles
            iCount = pNames.count(self.isotopes[i].shortName)
            #Append the data to the particleData list
            self.particleData[i].append(iCount)
            
    def clearVariables(self):
        """
        Resets all variables in case this class is called more than once.
        """
        self.time = 0
        self.step = 0
        
        self.isotopes.clear()
        self.particles.clear()
        self.particleData.clear()
        self.times.clear()
        self.steps.clear()
            
    def plotData(self):
        """
        Creates various plots using the data collected in the simulation.
        """
        #Attempt to create a directory with the name of the simulation
        try:
            os.mkdir(self.simulationName)
        except:
            pass
        
        #Create final data list that will be plotted
        finalData = []
        
        #Remove particleData entries that are empty (when particles are not present)
        for i in self.particleData:
            present = False
            for j in i:
                if j != 0:
                    present = True
            
            if present == True:
                finalData.append(i)
        
        #Create a stacked area plot showing how the numbers of each isotope change over time
        plt.stackplot(self.times, finalData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('t /s')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes over time (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
        plt.tight_layout()
        plt.plot()
        #Attempt to save a plot in the directory created earlier, otherwise save it in the same directory as this file
        try:
            plt.savefig(self.simulationName + "/time.png")
        except:
            plt.savefig(self.simulationName + "_time.png")
        plt.show()
        
        #Create a stacked area plot showing how the numbers of each isotope change between steps
        plt.stackplot(self.steps, finalData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('steps')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes per step (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
        plt.tight_layout()
        plt.plot()
        try:
            plt.savefig(self.simulationName + "/steps.png")
        except:
            plt.savefig(self.simulationName + "_steps.png")
        plt.show()
        
        #For each individual isotope, create a plot showing how its population changes over time
        for i in range(len(self.isotopes)):
            iName = self.isotopes[i].shortName
            plt.plot(self.times, self.particleData[i], "k-", label = iName)
            plt.xlabel('t /s')
            plt.ylabel('N')
            plt.legend()
            plt.title("Population of " + iName + " over time (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
            plt.tight_layout()
            plt.plot()
            try:
                plt.savefig(self.simulationName + "/" + iName + ".png")
            except:
                plt.savefig(self.simulationName + "_" + iName + ".png")
            plt.show()
        
        