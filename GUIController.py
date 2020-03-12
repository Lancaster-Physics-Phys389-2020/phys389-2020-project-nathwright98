# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:25:53 2020

@author: Nathan
"""

import tkinter as tk
from DecaySimulation import DecaySimulation
from Particle import Particle
from DecayMode import DecayMode
import csv
import ast
import copy

class GUIController:
    
    isotopes = []

    def __init__(self):
        self.initialiseIsotopes()
        
        gui = tk.Tk()
        gui.title('Nuclear Decay Simulation')
        
        nameLabel = tk.Label(gui, text = "Enter simulation name:")
        nameLabel.pack()
        
        nameText = tk.Text(gui, height = 2, width = 20)
        nameText.pack()
        nameText.insert(tk.END, "Simulation Name")
        
        listLabel = tk.Label(gui, text = "Select a simulation:")
        listLabel.pack()
    
        simulationList = tk.Listbox(gui, width = 25)
        simulationList.insert(0, 'Uranium-235')
        simulationList.insert(1, 'Uranium-238')
        simulationList.insert(2, 'Thorium-232')
        simulationList.pack()
        
        numberLabel = tk.Label(gui, text = "Enter the number of particles to simulate (N):")
        numberLabel.pack()
        
        numberText = tk.Text(gui, height = 2, width = 20)
        numberText.pack()
        numberText.insert(tk.END, "100")
        
        accuracyLabel = tk.Label(gui, text = "Select simulation accuracy (lower = more accurate):")
        accuracyLabel.pack()
        
        accuracyScale = tk.Scale(gui, from_=1.01, to = 3.00, resolution = 0.01, orient = tk.HORIZONTAL)
        accuracyScale.pack()

        startButton = tk.Button(gui, text = 'Start Simulation', width = 25, command = lambda: self.beginSimulation(nameText.get("1.0", tk.END), simulationList.curselection(), numberText.get("1.0", tk.END), accuracyScale.get()))
        startButton.pack()
        
        gui.mainloop()
        
    def __repr__(self):
        return 'GUI controller'
    
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
                        for x in row[5].split("&"):
                            #Remove the square brackets that are present for readability in the CSV file
                            x = x.strip("[]")
                            #Split the data into individual parts using ',' as the split point
                            dm = x.split(",", 2)
                            #Evaluate the data literally and create a DecayMode object using this data
                            decayModes.append(DecayMode(dm[0],dm[1],ast.literal_eval(dm[2])))
                    #If the half-life cell contains the string 'stable', the isotope is stable
                    else: stable = True
                    #Append a new Particle object to the 'isotopes' list
                    self.isotopes.append(Particle(row[0],row[1],eval(row[2]),eval(row[3]),eval(row[4]),decayModes,stable,2))
                    #Append a new empty list to the particleData list
                    #self.particleData.append([])
                #Increase the line count variable each time a line is read
                lineCount += 1
    
    def beginSimulation(self, name, simulationID, number, accuracyValue):
        particles = []
        N = int(number)
        accuracy = accuracyValue
        
        for i in self.isotopes:
            i.accuracy = accuracy
        
        if simulationID != None:
            smID = simulationID[0]
            particle = None
            if(smID == 0):
                particle = next((p for p in self.isotopes if p.shortName == "235U"), None)
            elif(smID == 1):
                particle = next((p for p in self.isotopes if p.shortName == "238U"), None)
            elif(smID == 2):
                particle = next((p for p in self.isotopes if p.shortName == "232Th"), None)
            for i in range(N):
                    particles.append(copy.copy(particle))
                    particles[i].isotopes = self.isotopes
            DecaySimulation(name, N, accuracy, self.isotopes, particles)