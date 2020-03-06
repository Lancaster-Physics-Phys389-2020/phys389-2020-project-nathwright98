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
    """
    Defines a simulation with given parameters which will then simulate the decay of a number of particles, continuing until all remaining particles are stable.
    """
    simulationName = "Simulation"
    time = 0
    step = 0
    N = 0
    
    particleData = []
    times = []
    steps = []
    
    isotopes = []
    particles = []

    def __init__(self, N):
        #Clear all remaining variables in case this class is called more than once.
        self.clearVariables()
        
        self.N = N
        #Define a list of isotopes
        self.initialiseIsotopes()
        #TEMPORARY: instantiate N particles with the same properties as the first isotope in the list
        for i in range(N):
            self.particles.append(copy.copy(self.isotopes[0]))
            self.particles[i].isotopes = self.isotopes
        #Start the simulation
        self.simulate()
        
    def __repr__(self):
        return "Decay Simulation"
    
    def initialiseIsotopes(self):
        """
        Defines a list of isotopes using data taken from a CSV file.
        """
        
        #Open the CSV file and read the data
        with open('isotopeData.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter = ',')
            lineCount = 0

            for row in csvReader:
                #Ignore first line as this corresponds to column titles, otherwise iterate through each row of data
                if lineCount > 0:
                    decayModes = []
                    #Define a boolean for stability of the particle, by default false
                    stable = False
                    #If the cell corresponding to half-life in the CSV file does not contain the string 'stable', look for decay modes in the appropriate cell
                    if(row[4] != "stable"):
                        #Split the string into individual decay modes, using '&' as the split point
                        for x in row[5].split("&", 1):
                            #Remove the square brackets that are present for readability in the CSV file
                            x = x.strip("[]")
                            #Split the data into individual parts using ',' as the split point
                            dm = x.split(",", 2)
                            #Evaluate the data literally and create a DecayMode object using this data
                            decayModes.append(DecayMode(dm[0],dm[1],ast.literal_eval(dm[2])))
                    #If the half-life cell contains the string 'stable', the isotope is stable
                    else: stable = True
                    #Append a new Particle object to the 'isotopes' list
                    self.isotopes.append(Particle(row[0],row[1],eval(row[2]),eval(row[3]),eval(row[4]),decayModes,stable))
                    #Append a new empty list to the particleData list
                    self.particleData.append([])
                #Increase the line count variable each time a line is read
                lineCount += 1
                
    def findLowestHalfLife(self):
        """
        Finds the particle in the list with the lowest half life, then returns this value.
        """
        tempParticles = []
        for p in self.particles:
            #Exclude stable particles as they have no half-life value
            if p.stable != True:
                tempParticles.append(p)
        return float(min(i.halfLife for i in tempParticles))
    
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
        timeToSimulate = self.findLowestHalfLife()
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
        
        #Create a stacked area plot showing how the numbers of each isotope change over time
        plt.stackplot(self.times, self.particleData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('t /s')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes over time (N = " + str(self.N) + ")")
        plt.tight_layout()
        plt.plot()
        #Attempt to save a plot in the directory created earlier, otherwise save it in the same directory as this file
        try:
            plt.savefig(self.simulationName + "/time.png")
        except:
            plt.savefig(self.simulationName + "_time.png")
        plt.show()
        
        #Create a stacked area plot showing how the numbers of each isotope change between steps
        plt.stackplot(self.steps, self.particleData, labels = list(i.shortName for i in self.isotopes))
        plt.xlabel('steps')
        plt.ylabel('N')
        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.title("Population of isotopes per step (N = " + str(self.N) + ")")
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
            plt.title("Population of " + iName + " over time (N = " + str(self.N) + ")")
            plt.tight_layout()
            plt.plot()
            try:
                plt.savefig(self.simulationName + "/" + iName + ".png")
            except:
                plt.savefig(self.simulationName + "_" + iName + ".png")
            plt.show()
        
        