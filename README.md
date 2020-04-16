# nuclear-decay
A program to simulate nuclear decay.

To run the program, run the RunGUI.py Python script. On a Windows machine with a valid installation of Python, this can be done by opening Command Prompt in the directory of the simulation files and entering the command 'python rungui.py'.

Upon running the program, a GUI will open which can be used to interact with the program. Be aware that there may be a small delay after running the script while the GUI loads. The GUI contains multiple interactive features through which you can customise the parameters of the simulation you wish to run.

The box labelled 'Enter simulation name' is a text box in which you can type a name for the simulation you are running, to help you identify the resulting plots at a later date. 

The list labelled 'Select a simulation' contains a list of all the simulations that are present in the program and that can be run. The name of the simulation corresponds to the isotope of which the original particles will have the properties.

The box labelled 'Enter the number of particles to simulate' is a box in which you can input the number of particles that you wish to simulate. This must be a positive integer greater than 0. Below this is a slider labelled 'Select simulation accuracy' in which you can adjust the level of accuracy you want the simulation to have, where a lower accuracy value results in a more accurate simulation. The slider is limited to prevent the simulation breaking.

The checkbox labelled 'Enable time limit' enables an optional feature of the simulation which stops the simulation after a certain amount of simulated time (note, this is not real time, but rather time that has passed in the simulation). If this is enabled, you can enter a time limit in seconds in the appropriately labelled box below. This is parsed as a float, so for example, '10000' could also be written as '1E4'. The percentage completion value displayed during a simulation does not factor in this time limit option. Additionally, if the time limit is greater than the duration of the complete simulation, the simulation will end before the time limit is reached.

The checkbox labelled 'Enable plotting of extra data' is responsible for enabling the plotting of extra graphs, specifically graphs of total atomic mass and total proton number, over the course of the simulation. These primarily are useful only for verifying that these quantities are being conserved correctly.

The 'Start Simulation' button can be pressed once all desired variables have been selected, and a simulation will be run with the selected parameters. A text box on the GUI will relay information on the status of the simulation back to you, such as any errors, as well as if the simulation is running, or if it has completed successfully. Upon successful completetion, this box will display the location to which the data plots have been saved. A percentage completion display will show you an approximation the percentage completion of the simulation.

At the end of a simulation, a list will be displayed showing how many particles of each isotope were present at the end of the simulation. In some cases, this list can be cut off. This seems to happen as a result of increased text size on Windows machines. This can be alleviated by resetting the text size to 100%.

The plots made by a simulation should be saved in an appropriately named directory alongside the simulation files. Otherwise, they will be saved individually alongside the simulation files.
