# Starter Engine Blender Factory
## Prerequisites
To use this tool, blender 2.90.1 must be used (the version is highly important!).
* Linux (with snap):
```console
sudo snap install blender --channel=2.90/stable --classic
```
* Windows: [Download-link](https://download.blender.org/release/Blender2.90/blender-2.90.0-windows64.msi)

In blender, the Add-Ons "BoltFactory" and "Extra Objects" must be activated. This can be done via: *Edit*>
*Preferences...*>*Add-ons*>Search for the Add-Ons and toggle them on

## How to use this software
### Blender-Start-Up
* Linux: Execute the `blender`-command in a terminal that is in the root directory of this repository. The terminal prompt's directory should end with `...starter_engine_blender_factory`.
* Windows: Configure blender to run in the root directory of this repository (has to be performed only once; German only):
  1. Type "blender" in the start-menu and wait for the program to show up (do not start it)
  2. Click "Dateispeicherort öffnen" on the right panel
  3. Right-click on the blender-link and click "Eigenschften"
  4. Set "Ausführen in" to the rrot directory of this repository (where the .py-files are located)
  
  Start blender normally.
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
