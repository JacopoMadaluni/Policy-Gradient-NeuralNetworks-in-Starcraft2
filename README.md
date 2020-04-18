# User guide
The project comes with two artifacts. <br />
The first runs the evaluator bot that plays Starcraft2. <br />
The second one can be used to train new policy gradients. <br />

## Prerequisites to run the artifacts

### Install Starcraft2
To run both the artifacts the Starcraft2 game is required. <br />
Every .zip file downloaded from the following github repository is password protected. <br />
The password is "iagreetotheeula". By typing that you will agree to the following AI and Machine Learning use license: http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html
#### On windows
- Download the full game for windows for free from the official Blizzard website https://starcraft2.com/en-gb/

On default settings, the game should be installed in the following location: C:\Program Files (x86)\StarCraft II\


#### On linux
Download the 4.7.1 linux version of Starcraft2 from the official repository https://github.com/Blizzard/s2client-proto#downloads <br />
The linux version does not come with GUI so it won't be possible to see the interface of the game while the program is running.

The linux version will be installed on whatever folder the .zip file was extracted to. (e.g /home/User/Starcraft II)



### Install NVIDIA Cuda (both Windows and Linux)
In order for the neural network to be loaded, NVIDIA Cuda 10.2 is required.
- Make sure that the GPU of the system is "CUDA-capable"
- Make sure the system has a supported version of Microsoft Visual Studio (only on windows, visual studio is required because of some dependencies)
- Download CUDA from the following official website: https://developer.nvidia.com/cuda-downloads
- If something goes wrong with the installation or the artifacts crash because of CUDA errors, be sure to check the official CUDA installation guide: https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html


### Install Anaconda and set up virtual environment.
Anaconda is used in this project to handle dependencies. <br />
Anaconda can be downloaded for both windows and linux on the official website: https://www.anaconda.com/distribution/ <br />
Be sure to use the Python 3.7 version. <br />
Once Anaconda is successfully installed, import the environment by using:
```conda env create -f environment.yml``` on Linux or Gitbash on windows
where the environment.yml file is the file contained in the same folder of this markdown.
Alternatively, you can import the environment by going into the Anaconda navigator -> Environments -> Import. <br />
Select the same environment.yml file to be imported.  <br />
<br />
Once the environment is successfully imported. Activate it with the following command: <br />
On Windows: ```activate starcraft2_env```  <br />
On Linux ```source activate starcraft2_env``` <br />

#### Ensure that the library paths are correctly configured
Once the Anaconda environment has been loaded, follow these steps.
C:\Users\Jaco\Anaconda3\envs\FinalProjectTraining\Lib\site-packages\sc2
- Go to the Anaconda folder (on Windows, the default is "C:\Users\USER\Anaconda3")
- Once in the Anaconda folder go to envs\starcraft2_env\Lib\site-packages\sc2
- In this folder there is a library file called "paths.py" that contains various pointers to the game paths. 
- Make sure that the paths contained in the file match with the paths of your system. In particular:

```
BASEDIR = {
    "Windows": "C:/Program Files (x86)/StarCraft II",  # Windows path to Starcraft II folder, change accordingly
    "Darwin": "/Applications/StarCraft II",
    "Linux": "~/StarCraftII",                          # Linux path to Starcraft II folder, change accordingly
    "WineLinux": "~/.wine/drive_c/Program Files (x86)/StarCraft II",
}

USERPATH = {
    "Windows": "\\Documents\\StarCraft II\\ExecuteInfo.txt",
    "Darwin": "/Library/Application Support/Blizzard/StarCraft II/ExecuteInfo.txt",
    "Linux": None,
    "WineLinux": None,
}

BINPATH = {
    "Windows": "SC2_x64.exe",   # Windows name for the Starcraft II binary executable. If default fails, change accordingly
    "Darwin": "SC2.app/Contents/MacOS/SC2",
    "Linux": "SC2_x64",         # Linux name for the Starcraft II binary executable. If default fails, change accordingly
    "WineLinux": "SC2_x64.exe",
}
```

### Set up required Starcraft2 maps
Assuming Starcraft2 is already installed in the system, the path to the folder should look something like this: <br />
On windows: C:\Program Files (x86)\StarCraft II\ <br />
On linux: /home/User/.../Starcraft II <br />

- Download the Ladder 2017 Season 1 maps folder from https://github.com/Blizzard/s2client-proto#downloads
    Like stated before, the .zip is protected by the "iagreetotheeula" password.

- Make sure that:
    - It exists a "Maps" (capital M) folder inside the StarCraft II folder. If it does not exist, create one.
    - Move the previously downloaded Ladder 2017 Season 1 folder and copy it into the "Maps" folder.
It should now exist a folder "...\StarCraft II\Maps\Ladder2017Season1" containing the AbyssalReefLE.SC2Map file.     


- Create a folder "CustomMaps" (the name of this folder does not matter) inside the "Maps" folder. The following path should not exist: ...      \StarCraft II\Maps\CustomMaps
- From the folder where this readme is contained go to TrainingEnvironment/maps. Inside the maps folder you should find a TraningEnvironment.SC2Map file. 
- Copy the TraningEnvironment.SC2Map file and paste it into the "CustomMaps" folder.

It should now exist a folder "...\StarCraft II\Maps\CustomMaps" containing the TraningEnvironment.SC2Map file. <br />
This is the simulated environment where the neural network trains.


## First artifact - Training a new policy gradient
To begin with, make sure that the virtual environment is active. <br />
From the main folder of this project, the first artifact can be executed with the following commands: <br />
- ```cd TrainingEnvironment```
- ```python main_train```
The console will ask for a save location. The save location refers to a folder contained in ./TrainingEnvironment/neural_training/checkpoints/ <br />
If the location typed exists, the prompt will ask if the user wishes to load the already existing gradient. <br />
If the location does not exist, a new gradient will be initialized. The prompt will ask the user to either keep the default settings or set new settings. <br />

After the gradient is initialized, the prompt will ask the user what kind of units the network can use. Feel free to randomly choose some of them, few of them, or all of them. <br />

Once this is done, the prompt will ask how many episodes must be run. <br />
After inputting the number of episodes the training will start. Feel free to stop the process (CTRL+C), the progress is saved at the end of each episode. <br />

Example: 
```
Choose save location
> test
Do you want to use the following default settings? [y/n]
 - alpha = 0.01
 - gamma = 0.99
 - layer 1 and 2 size = 128
> n
Input learning ratio alpha (suggested: 0.01)
> 0.5
Input discount factor gamma (0 <= gamma < 1)
> 0.3
Input number of first hidden layer neurons (best: 128)
> 16
Input number of second hidden layer neurons (best: 128)
> 64
Press [y/n] to choose which units the agent can use to counter the enemy army.

Use probe? [y/n]
> n
Use zealot? [y/n]
> y
Use sentry? [y/n]
> y
Use stalker? [y/n]
> y
Use adept? [y/n]
> y
Use ht? [y/n]
> y
Use dt? [y/n]
> y
Use archon? [y/n]
> n
Use immortal? [y/n]
> y
Use colossus? [y/n]
> y
Use phoenix? [y/n]
> n
Use voidray? [y/n]
> y
Use tempest? [y/n]
> n
Use carrier? [y/n]
> y
Initialized following namespace: [UnitTypeId.ZEALOT, UnitTypeId.SENTRY, UnitTypeId.STALKER, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.VOIDRAY, UnitTypeId.CARRIER]
Proceed? [y/n]
> y

How many simulations?
> 10
```


## Second artifact - Running the main agent
This artifact will run the agent that plays a full game of Starcraft2, using a network to choose what units to employ. <br />
The artifacts can be run by running: <br />
```python main.py``` from the main folder (the one containing this file) <br />
The prompt will ask for the opponent difficulty [easy, medium, hard, vhard]. <br />
After that, the prompt will ask if the game will be speed up. If yes ("y") the game will run as fast as possible. <br />
If no ("n") the game will run at human speed, making it easier (and slower) to watch the game being played. <br />
At last, the prompt will ask which network to load, either the default one, or a specific one inputted by the user. <br />
The input is expected to be the name of a folder inside ./TrainingEnvironment/neural_training/checkpoints/ <br />
Example: 
```
Input difficulty [easy, medium, hard, vhard]
> easy
Do you want the game to be speed up? [y,n]
> y
The default trained network will be used by default. Do you want to change it? [y/n]
> y
Please specify the name of the gradient folder (case sensitive)
> test_network
```







