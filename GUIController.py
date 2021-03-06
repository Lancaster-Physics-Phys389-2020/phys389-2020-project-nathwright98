# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:25:53 2020

@author: Nathan
"""

import tkinter as tk
from DecaySimulation import DecaySimulation
from ComplexParticle import ComplexParticle
from DecayMode import DecayMode
import csv
import ast
import copy
import os

class GUIController:
    """
    Creates a GUI through which the user can define variables for a simulation which they can then run.
    """
    isotopes = []
    
    master = None
    infoText = None
    
    enableTimeLimit = None
    extraPlots = None
    
    percentageText = None
    resultsText = None

    def __init__(self):
        self.initialiseIsotopes()
        
        #Create the GUI
        gui = tk.Tk()
        self.master = gui
        #Title the GUI window
        gui.title('Nuclear Decay Simulation')
        
        nameLabel = tk.Label(gui, text = "Enter simulation name:")
        nameLabel.pack()
        
        #Create a box in which the user can define a name for their simulation
        nameText = tk.Text(gui, height = 2, width = 20)
        nameText.pack()
        nameText.insert(tk.END, "Simulation Name")
        
        listLabel = tk.Label(gui, text = "Select a simulation:")
        listLabel.pack()
    
        #Create a list of simulations the user can pick from
        simulationList = tk.Listbox(gui, width = 25)
        simulationList.insert(0, 'Uranium-235')
        simulationList.insert(1, 'Uranium-238')
        simulationList.insert(2, 'Thorium-232')
        simulationList.insert(3, 'Protactinium-231')
        simulationList.insert(4, 'Neptunium-237')
        simulationList.insert(5, 'Neptunium-239')
        simulationList.insert(6, 'Americium-241')
        simulationList.insert(7, 'Curium-247')
        simulationList.insert(8, 'Silicon-22')
        simulationList.pack()
        
        numberLabel = tk.Label(gui, text = "Enter the number of particles to simulate (N):\n[Large N can take a long time]")
        numberLabel.pack()
        
        #Allow the user to select how many particles they wish to simulate
        numberText = tk.Text(gui, height = 2, width = 20)
        numberText.pack()
        numberText.insert(tk.END, "100")
        
        accuracyLabel = tk.Label(gui, text = "Select simulation accuracy (lower = more accurate):\n[Low accuracy can take a long time]")
        accuracyLabel.pack()
        
        #Allow the user to define an accuracy for the simulation
        accuracyScale = tk.Scale(gui, from_=1.01, to = 3.00, resolution = 0.01, orient = tk.HORIZONTAL)
        accuracyScale.pack()
        
        self.enableTimeLimit = tk.BooleanVar()
        #Create a check box to allow the user to enable a time limit, stopping the simulation after a certain time
        checkBox = tk.Checkbutton(gui, text = 'Enable time limit (stops the simulation after a certain simulated time)', variable = self.enableTimeLimit)
        checkBox.pack()
        
        numberLabel = tk.Label(gui, text = "Enter the time limit (in seconds) you would like:\n[Note this will only take effect if you have checked the box above and that the\npercentage completion does not account for stopping the simulation early]")
        numberLabel.pack()
        
        #Allow the user to select a time limit, if necessary
        timeLimitText = tk.Text(gui, height = 2, width = 20)
        timeLimitText.pack()
        timeLimitText.insert(tk.END, "N/A")
        
        self.extraPlots = tk.BooleanVar()
        #Create a check box to allow the user to enable plotting of extra data
        checkBox = tk.Checkbutton(gui, text = 'Enable plotting of extra data \n[This may slow down the simulation]', variable = self.extraPlots)
        checkBox.pack()
        
        #Create a text box where information on the status of the simulation can be provided to the user
        self.infoText = tk.Label(gui)
        self.infoText.pack()
        
        #Create a text box to show percentage completion
        self.percentageText = tk.Label(gui)
        self.percentageText.pack()
        
        #Create a start button which, upon being pressed, will run the beginSimulation function
        startButton = tk.Button(gui, text = 'Start Simulation', width = 25, command = lambda: self.beginSimulation(nameText.get("1.0", tk.END), simulationList.curselection(), numberText.get("1.0", tk.END), accuracyScale.get(), timeLimitText.get("1.0", tk.END)))
        startButton.pack()
        
        #Create a text box to show final isotope counts
        self.resultsText  = tk.Label(gui)
        self.resultsText.pack()
        
        #Run the main loop of the GUI
        gui.mainloop()
        
    def __repr__(self):
        return 'GUI controller'
    
    def initialiseIsotopes(self):
        """
        Defines a list of isotopes using data taken from a CSV file.
        """
        #Reset list of isotopes incase this function is run twice
        self.isotopes.clear()
        
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
                    self.isotopes.append(ComplexParticle(row[0],row[1],eval(row[2]),eval(row[3]),eval(row[4]),decayModes,stable,2))
                    #Append a new empty list to the particleData list
                    #self.particleData.append([])
                #Increase the line count variable each time a line is read
                lineCount += 1
    
    def beginSimulation(self, name, simulationID, number, accuracyValue, selectedTimeLimit):
        """
        Begins the simulation by defining the initial variables and passing them to an instance of the DecaySimulation class.
        """
        #Sanitise name input such that it can be used as a filename
        trueName = "".join(x for x in name if x.isalnum())
        
        particles = []
        
        #Try to set N to be an integer equal to the selected value
        try:
            N = int(number)
        except:
            N = None
        
        timeLimit = None
        #If the option is checked, try to set timeLimit to a float equal to the selected value
        if(self.enableTimeLimit.get() == True):
            try:
                timeLimit = float(selectedTimeLimit)
            except:
                pass
        
        accuracy = accuracyValue
        
        #Pass each defined isotope the accuracy value, so that the generated particles can reference this during initialisation
        for i in self.isotopes:
            i.accuracy = accuracy
        
        #Define a variable to determine the ID of the selected simulation
        smID = None
        
        #If no simulation was selected, display an error message
        if len(simulationID) == 0:
            smID = None
            self.displayMessage('error', 'ERROR: No simulation selected.')
        #If N is not a number, trigger an error message
        elif(N == None):
            self.displayMessage("error", "ERROR: Invalid number of particles. Please type an integer value.")
        #If N is less than 1, trigger an error message
        elif(N < 1):
            self.displayMessage("error", "ERROR: N must be at least 1.")
        #If the time limit was enabled, check the value is a valid float
        elif(self.enableTimeLimit.get() == True and timeLimit == None):
            self.displayMessage("error", "ERROR: Time limit is not a valid float.")
        #If the time limit was enabled, check the value is greater than 0
        elif(self.enableTimeLimit.get() == True and timeLimit <= 0):
            self.displayMessage("error", "ERROR: Time limit must be greater than 0.")
        #If a simulation was selected, and N is a valid integer greater than 0, assign the corresponding ID to the smID variable, and inform the user the simulation is running
        else: 
            smID = simulationID[0]
            self.displayMessage('info', 'Simulation running...')
        
        #If a valid simulation was selected, populate the list of particles to simulate
        if (smID != None):
            particle = None
            #Select the particle type based on the ID of the simulation
            if(smID == 0):
                particle = next((p for p in self.isotopes if p.shortName == "235U"), None)
            elif(smID == 1):
                particle = next((p for p in self.isotopes if p.shortName == "238U"), None)
            elif(smID == 2):
                particle = next((p for p in self.isotopes if p.shortName == "232Th"), None)
            elif(smID == 3):
                particle = next((p for p in self.isotopes if p.shortName == "231Pa"), None)
            elif(smID == 4):
                particle = next((p for p in self.isotopes if p.shortName == "237Np"), None)
            elif(smID == 5):
                particle = next((p for p in self.isotopes if p.shortName == "239Np"), None)
            elif(smID == 6):
                particle = next((p for p in self.isotopes if p.shortName == "241Am"), None)
            elif(smID == 7):
                particle = next((p for p in self.isotopes if p.shortName == "247Cm"), None)
            elif(smID == 8):
                particle = next((p for p in self.isotopes if p.shortName == "22Si"), None)
            #Add the chosen number of the selected particle type
            for i in range(N):
                    particles.append(copy.copy(particle))
                    #Pass the list of isotopes to each particle so that it can be referenced
                    particles[i].isotopes = self.isotopes
            #Run the decay simulation by calling the DecaySimulation class
            DecaySimulation(trueName, N, accuracy, self.isotopes, particles, timeLimit, self.extraPlots.get(), self.master, self.percentageText, self.resultsText)
            
            #Once the simulation is complete, display a success message and show the location in which the plots have been saved
            if(os.path.isdir(os.getcwd()+'\\'+trueName) == True):
                self.displayMessage('success', 'Simulation complete! \rPlots saved in ' + os.getcwd() + '\\' + trueName)
            else: self.displayMessage('success', 'Simulation complete! \rPlots saved in ' + os.getcwd())
            
    def displayMessage(self, msgType, msgText):
        """
        Writes a message of the selected message type (error, information, or success) in the information text box.
        """
        #Select a colour for the text depending on the type of message
        if msgType == 'error':
            colourID = 'red'
        elif msgType == 'info':
            colourID = 'orange'
        elif msgType == 'success':
            colourID = 'green'
        
        #Set the text colour
        self.infoText['fg'] = colourID
        #Set the contents of the text box
        self.infoText['text'] = msgText
        #Update the UI
        self.master.update()