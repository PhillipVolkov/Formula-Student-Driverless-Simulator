# Getting started

When running this simulator there are two steps: running the simulator and connecting your autonomous system.
This page helps you run the simulation.
After you have finished this page you can go on and connect your autonomous system. 

To run the simulation smoothly you need quite a fast Windows computer with a modern videocard.
We highly recommend the following computer specs. 
You might be able to run with less power but everything will be slower.
For developing this project, you need quite a good computer because Unreal Engine is a heavy baby.

* 8 core 2.3Ghz CPU
* 12 GB memory
* 30GB free SSD storage (120GB when building the unreal project from source)
* Recent NVidia card with Vulkan support and 3 GB of memory. (You can check the video card drivers by running `vulkaninfo`). Different brand video cards might work but have not been tested.

If your computer does not suffice you can use a remote workstation on Google Cloud Platform.
Read [this tutorial](gcp-remote-workstation.md) on how to setup your virtual workstation.

## Settings

In order to work, the simulator requires a `settings.json` file, which contains general settings and the sensor configuration of the car.
The simulator will look for this file in the following places:
- `~/Formula-Student-Driverless-Simulator/settings.json` in your **home directory**,
- The folder the simulator binary is located in (`<the folder with FSDS.sh>/FSOnline/Binaries/<your OS>/`). 
- The current working directory when the simulator binary is launched
- The path supplied via the `-settings "<path to settings.json file>` command line argument to the binary

Alternatively, when programatically generating the setttings, the simulator also accepts
the settings as a URL encoded json string (e.g. `-settings "%7B%22SeeDocsAt%22%3A%22https%....`)

If you cloned the repo in your home directory you will already have this file in place.
If not, copy-paste the contents of the [settings.json file at the root of this repository](https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator/blob/master/settings.json) into the `~/Formula-Student-Driverless-Simulator`.
This should get you started with the default vehicle and sensor configuration, but feel free to try your own custom sensor suite.
The default vehicle is the Technion Formula Student racing car, but teams participating in the UK edition of FS-AI might want
to simulate the ADS-DV vehicle. To do so, change the value of the `PawnBP` field in `settings.json` to `"Class'/AirSim/VehicleAdv/Cars/AdsDv/AdsDv_Pawn.AdsDv_Pawn_C'"`.

## Installation 

### From release binaries

Pre-compiled binaries are available for every release.
Go to [releases](https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator/releases) and download the latest one.
Unzip it to anywhere on your computer and launch FSDS.exe.
A window with a car should popup!
Try driving the car around using the arrowkeys.
If you get a black screen with some buttons, make sure the folder with the binary is in your user folder (Windows: `C:\Users\username\Formula-Student-Driverless-Simulator`, Linux: `~/Formula-Student-Driverless-Simulator`)

If all that works, you can continue to [the ROS interface](getting-started-with-ros.md) or [the python interface](getting-started-with-python.md).

### From source using the Unreal Engine Editor
Instead of running the simulator from release binaries, you can compile it manually using unreal engine.
This is usefull if you want to get the latest changes or if you want to make changes to the maps or the simulation itself.
If you want to run the unreal engine project from source you will need [unreal engine and visual studio 2019](software-install-instructions.md).
On Ubuntu you can skip the visual studio 2019 part, but you still need Unreal Engine.

#### 1. Get the repository

You can either download the repo using the big green download button on the [github page of this project](https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator) or clone the repository. For cloning, checkout the documentation on this further down this page. Make sure you clone the repository in your **home directory** and git **submodules** are included:

```
git clone https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator.git --recurse-submodules
```

When downloading or cloning, by default you get the latest, unreleased version. This is probably not the version that you want. Make sure you select the version that you need! 

#### 2. Compiling the AirSim plugin
The Unreal Engine project requires the AirSim plugin.
We have to compile this plugin first.
The AirSim plugin is made up of AirLib (/AirSim/AirLib) and the plugin code (/UE4Project/Plugins/AirSim/Source).
AirLib is the shared code between the ros wrapper and the AirSim Unreal Engine plugin.

First build the AirLib code.

On Windows, open the _Developer Command Prompt for VS 2019_, go to `Formula-Student-Driverless-Simulator/AirSim` and run
```
build.cmd
```

On Ubuntu 18.04 and 20.04, go to folder `AirSim` and run `setup.sh` and `build.sh`.

##### For Ubuntu 22.04+
**Written by Roy Amoyal, Head of the Autonomous Division at BGRacing 2024 (Formula Student Driverless Project at Ben Gurion University)**
First, install Docker on your Ubuntu system.

Change to the Docker Build Directory: Note that this directory is within the AirSim folder, not the root of the Formula-Student-Driverless-Simulator repository.

    cd /home/$USER/Formula-Student-Driverless-Simulator/AirSim/docker_build

1. Build the Docker Image:

        docker build -t formula-simulator .

2. Run the Docker Container: After the build completes, mount your local folder into the container:

        docker run --rm -it -v $PWD/../..:/home/airsim/Formula-Student-Driverless-Simulator formula-simulator

3. Run the Setup and Build:

       ./setup.sh && ./build.sh

4. Exit the Docker Container: Press Ctrl + D in the terminal to exit.

5. Build the final project, use the following command (this process may take some time):

       ~/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono ~/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/home/$uSER/Formula-Student-Driverless-Simulator/UE4Project/FSOnline.uproject -TargetType=Editor -Progress

Congratulations! You have successfully built the project from source. You can now continue with Unreal Engine.


> So what does build.cmd or setup.sh+build.sh do? 
  It downloads any nessesary libraries and compiles AirLib.
  After compilation it places the files in the UE4Project so that these files can be used durcing compilation of the plugin.

The first time this takes quite a while. Go walk around a bit, maybe start playing [factoryidle](https://factoryidle.com/). 

#### 3. Working with the Unreal Engine project

Launch Unreal Engine, press Browse and open the FSDS project in `~/Driverless-Competition-Simulator/UE4Project/FSOnline.uproject`. 
The project should now open correctly. 
If it does not, make sure of the following:

 * you have cloned the repository inside your home folder (~/) 
 * you have cloned with LFS enabed. If not, run `git lfs install` and `git lfs pull` to download the large files.
 * within `~/Driverless-Competition-Simulator/AirSim/`, you have run `build.cmd` on Windows and `./setup.sh && ./build.sh` on Ubuntu.

On Ubuntu, we recommend adding the following alias to your `~/.bashrc` to speed up the process of opening the repository in the future:
`alias ue='~/UnrealEngine/Engine/Binaries/Linux/UE4Editor ~/Formula-Student-Driverless-Simulator/UE4Project/FSOnline.uproject'`

It might show an error like 'This project was made with a different version of the Unreal Engine'. In that case select `more options` and `skip conversion`.

When asked to rebuild the 'Blocks' and 'AirSim' modules, choose 'Yes'.
This is the step where the plugin part of AirSim is compiled.

After some time Unreal Engine will start and you can launch the game. 
Run the game in standalone mode or or selected viewport mode, simulate and eject mode do not support camera's.

If you make changes to AirLib you have to run `build.cmd` again.

If you make changes to the plugin code or AirLib, you only have to recompile the plugin.
This can be done from within the Unreal Editor. go to to `Window` -> `Developer tools` -> `Modules`.
Search for `AirSim` and click `Recompile`.

#### 4. Launching the game

To run the game, click the big Play button.
If you want to run it like it would run when packaged, choose 'Run as standalone game'.

## Next steps
Now you are ready to connect your autonomous system.
At the moment there are two integration methods:

* [Use the ROS bridge](getting-started-with-ros.md) to connect your ROS autonomous system to the bridge.
* [Use the Python client](getting-started-with-python.md) to interact with the simulator.
