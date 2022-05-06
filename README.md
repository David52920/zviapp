# ZVIAPP

<h4><i>This project is meant to be a public version of engineering application I created, company specific info has been removed (logos, algorithms, etc..). Therefore application is not functional but as a whole does indeed work</i></h4>

# GUI
<img src=./doc-images/dark-app.PNG>

# Folder Structure

<img src=./doc-images/folder-structure.PNG>

#### Brief folder description:
<div>

1. [common](src/common) - package for all window-like objects
2. [common.managers](src/common/managers) - managers to control certani aspects of program (email manager deals with emailing)
3. [common.threads](src/common/threads) - basic Qt threads to allow multi-tasking
4. [common.widgets](src/common/widgets) - custom Qt widgets (QLineEdit, QComboBox, etc)
5. [common.windows](src/common/windows) - packages for all subwindows
6. [constants](src/constants) - application constants
7. [assets](src/assets) - assets/resources to make the program work (icons/images)
8. [util](src/util) - basic utility functions to make coding easier without duplication

</div>


# Features
- update within application
- theme selection
- save/restore state
- stage matching automation
- private
- in-app web browser
- mail program - easily send/cc email to members of outlook
- application shortcuts
- customer project creation (creates folders/adds templates)

# Settings and Customizations
<i>ZVIApp provides user a way to customize the theme, variables and optionally choose between directories all in one tabbed-window.</i>

## Theme
<img src=./doc-images/theme-app.PNG>

- Themes are changed via `Settings` window `Themes` tab.
  - Custom colors can be selected via the `Add Custom Theme` button as shown.

## Variables
<img src=./doc-images/variables-app.PNG>

- Variables are changed via `Settings` window `Variables` tab.
  - User has option to choose between local/server located startup files.
  - To change the variables; simply click on the selected value column and enter in value.

## Directories
<img src=./doc-images/directories-app.PNG>

- Directories are changed via `Settings` window `Directories` tab.
  - User can change working directories; while adding them to a list; for reuse later on.


# Updating Application
User now has the option to download/update their App. Some user input is required.

A message will be flashed on the bottom edge of the application to verify if there is an update. 

Simply click on the `Check for Updates...` button and user will be prompted to continue update process if an update is available, otherwise will show that the application is current.

<img src=./doc-images/update-app.PNG>

<i>Otherwise user can download application files manually via same way they installed the application to their system.</i>

# Automated Build Process

1. Run buildtool file
 ```~\.wbuildtool.bat```

<i>Build file locations are hardcoded; to change locations you must edit the [setup](setup.py) and [buildtool](wbuildtool.bat) files.</i>
"# zviapp" 
