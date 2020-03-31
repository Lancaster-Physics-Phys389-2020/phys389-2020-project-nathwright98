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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np
from Particle import Particle
import sys
import os

class DecaySimulation():
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
    
    totalA = []
    totalZ = []
    
    isotopes = []
    particles = []
    decayParticles = []
    
    timeLimit = None
    extraPlots = False
    
    gui = None
    percentageText = None
    resultsText = None

    def __init__(self, name, N, accuracy, isotopes, particles, timeLimit, enableExtraPlots, gui, pText, rText):
        #Clear all remaining variables in case this class is called more than once.
        self.clearVariables()
        
        self.simulationName = name
        
        self.N = N
        self.accuracy = accuracy
        
        #Allow this class to access the list of isotopes
        self.isotopes = isotopes
        #For each isotope, add an empty list to the particleData list
        for i in isotopes:
            self.particleData.append([])
        #Define the list of particles that the simulation will use, based on the list that is passed to this class
        self.particles = particles
        
        self.timeLimit = timeLimit
        self.extraPlots = enableExtraPlots
        print(self.timeLimit)
        
        #Assign variables relating to the GUI, used to provide a percentage completion
        self.gui = gui
        self.percentageText = pText
        self.resultsText = rText
        
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
        Checks if the simulation is complete by checking if all the particles are stable, or if the time limit has been reached, also calculates a percentage completion.
        """
        if(self.timeLimit != None and self.time >= self.timeLimit):
            return True
        #Calculate number of stable particles
        nStable = sum(i.stable == True for i in self.particles)
        #Calculate percentage completion
        percentComplete = 100 * nStable / self.N
        #Print percentage completion to terminal
        sys.stdout.write("\r")
        sys.stdout.write(str(percentComplete))
        sys.stdout.flush()
        #If GUI is being used, update the GUI with percentage completion
        if(self.percentageText != None):
            self.percentageText['text'] = ("Percentage completion: " + str(percentComplete) + "%")
            self.gui.update()
        
        #If not all particles are stable, return False, else return True
        if(nStable < self.N):
            return False
        else: return True
    
    def simulate(self):
        """
        Runs the simulation until all the particles are stable.
        """
        #Record data before the first step of the simulation takes place
        self.addData()
        #While there are still unstable particles, or the time is less than the time limit, continue simulating time steps
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
                #Decrement the timeRemaining variable of the particle, return true if it should decay
                if p.setTimeRemaining(p.timeRemaining - timeToSimulate) == True:
                    #Set a list of decay products as the returned list from the checkDecay function, which will be None if the particle does not decay
                    decayParticles = p.checkDecay()
                    #If such decay products exist, record data about them
                    if decayParticles != None:
                        self.recordProducts(decayParticles)
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
        #If extra plots are enabled, record data on atomic mass and atomic number to verify the simulation works correctly
        if self.extraPlots == True:
            totalAcount = 0
            totalZcount = 0
            #Iterate through particles to find total values
            for p in self.particles:
                totalAcount += p.massNumber
                totalZcount += p.atomicNumber
            #Iterate through decay products to find total values
            for p in self.decayParticles:
                totalAcount += p.massNumber
                totalZcount += p.atomicNumber
            self.totalA.append(totalAcount)
            self.totalZ.append(totalZcount)
            
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
        self.totalA.clear()
        self.totalZ.clear()
        
    def particleDataCheck(self, i):
        """
        Checks the particle data to see if a given entry is empty, indicating that the particle is not present.
        """
        present = False
        for j in self.particleData[i]:
            if j != 0:
                present = True
        return present
    
    def recordProducts(self, decayParticles):
        """
        Record data about the decay products of a particle which has decayed
        """
        #Define particles to add to the list based on the decay products value
        if(decayParticles == "a"):
            self.decayParticles.append(Particle("Alpha [He2+]", "a", 4, 2))
        elif(decayParticles == "b-"):
            self.decayParticles.append(Particle("Beta- [Electron]", "b-", 0, -1))
        elif(decayParticles == "b+"):
            self.decayParticles.append(Particle("Beta+ [Positron]", "b+", 0, 1))
        elif(decayParticles == "b-a"):
            self.decayParticles.append(Particle("Beta- [Electron]", "b-", 0, -1))
            self.decayParticles.append(Particle("Alpha [He2+]", "a", 4, 2))
        elif(decayParticles == "b+a"):
            self.decayParticles.append(Particle("Beta+ [Positron]", "b+", 0, 1))
            self.decayParticles.append(Particle("Alpha [He2+]", "a", 4, 2))
        elif(decayParticles == "b+p"):
            self.decayParticles.append(Particle("Beta+ [Positron]", "b+", 0, 1))
            self.decayParticles.append(Particle("Proton", "p", 1, 1))
        elif(decayParticles == "b+2p"):
            self.decayParticles.append(Particle("Beta+ [Positron]", "b+", 0, 1))
            self.decayParticles.append(Particle("Proton", "p", 1, 1))
            self.decayParticles.append(Particle("Proton", "p", 1, 1))
            
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
        #Create corresponding list of isotopes which appear in the data
        finalIsotopes = []
        
        #Remove particleData entries that are empty (when particles are not present)
        for i in range(len(self.particleData)):
            if self.particleDataCheck(i) == True:
                finalData.append(self.particleData[i])
                finalIsotopes.append(self.isotopes[i])
        
        #Create an empty string to populate with data about results        
        results = ""
        #Iterate through each isotope and append the count to the results string
        for i in range(len(finalIsotopes)):
            results += (finalIsotopes[i].Name + ": " + str(finalData[i][-1]) + "\r")
        #Display the results string on the GUI, if it exists
        if(self.resultsText != None):
            self.resultsText['text'] = results
            self.gui.update()
        
        #Initialise a colour list to use in the plots, avoiding repeated colours
        colours = plt.cm.rainbow(np.linspace(0,1,len(finalIsotopes)))   
        plt.rc('axes', prop_cycle = (cycler('color', colours)))
        #Set the figure size
        plt.rcParams["figure.figsize"] = (8,6)
        
        #Create a stacked area plot showing how the numbers of each isotope change over time
        plt.stackplot(self.times, finalData, labels = list(i.shortName for i in finalIsotopes))
        plt.xlabel('t /s')
        plt.ylabel('N')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
        plt.title("Population of isotopes over time (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
        plt.tight_layout()
        plt.plot()
        #Attempt to save a plot in the directory created earlier, otherwise save it in the same directory as this file
        try:
            plt.savefig(self.simulationName + "/time.png")
        except:
            plt.savefig(self.simulationName + "_time.png")
        plt.close()
        
        #Create a stacked area plot showing how the numbers of each isotope change between steps
        plt.stackplot(self.steps, finalData, labels = list(i.shortName for i in finalIsotopes))
        plt.xlabel('steps')
        plt.ylabel('N')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
        plt.title("Population of isotopes per step (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
        plt.tight_layout()
        plt.plot()
        try:
            plt.savefig(self.simulationName + "/steps.png")
        except:
            plt.savefig(self.simulationName + "_steps.png")
        plt.close()
        
        #For each individual isotope, create a plot showing how its population changes over time
        for i in range(len(finalIsotopes)):
            iName = finalIsotopes[i].shortName
            plt.plot(self.times, finalData[i], "k-", label = iName)
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
            plt.close()
        
        #If user enabled the extra plots option, create these plots
        if self.extraPlots == True:
            #Create a plot showing total atomic mass number over time
            plt.plot(self.times, self.totalA, "k-", label = "total atomic mass (A)")
            plt.xlabel('time /s')
            plt.ylabel('A')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
            plt.title("Total atomic mass number across time (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
            plt.tight_layout()
            plt.plot()
            try:
                plt.savefig(self.simulationName + "/totalA.png")
            except:
                plt.savefig(self.simulationName + "_totalA.png")
            plt.close()
        
            #Create a plot showing total atomic (proton) number over time
            plt.plot(self.times, self.totalZ, "k-", label = "total atomic number (Z)")
            plt.xlabel('time /s')
            plt.ylabel('Z')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
            plt.title("Total atomic (proton) number across time (N = " + str(self.N) + ", accuracy = " + str(self.accuracy) + ")")
            plt.tight_layout()
            plt.plot()
            try:
                plt.savefig(self.simulationName + "/totalZ.png")
            except:
                plt.savefig(self.simulationName + "_totalZ.png")
            plt.close()
