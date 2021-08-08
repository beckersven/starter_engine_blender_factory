# Starter Engine Blender Factory
## Prerequisites
To use this tool, blender 2.90.1 must be used. It can be installed via 
```console
sudo snap install blender --channel=2.90/stable --classic
```
In blender, the Add-Ons "BoltFactory" and "Extra Objects" must be activated. This can be done via: *Edit*>
*Preferences...*>*Add-ons*>Search for the Add-Ons and toggle them on

## How to use this software
### Blender-Start-Up
Execute the `blender`-command in a terminal that is in the root directory of this repository. The terminal prompt's directory should end with `...starter_engine_blender_factory`.
### Loading the Add-On
1. Compress this repository locally into a `.zip`-file. This can usually be done with the context menu in the file manager's GUI.
2. Go in Blender to the Add-On-Settings and install this Add-On by selecting the generated `.zip`-file in the selector: *Edit*>
*Preferences...*>*Add-ons*>*Install...*
3. Activate this Add-On
### Creating a Motor
There are multiple options:
* Via GUI (in object mode): *Add*>*Mesh*>*Starter Engine*
* Via command (F3): Type 'starter engine properties' and hit Enter

Expand and use the menu in the bottom left corner to customize the motor.
