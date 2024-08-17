# Pypulous

A recreation of the original Populous in Python

Still in it's very early stages.

## Dependancies

Get the latest Python implimentation for you environment
   
    http://www.python.org/download/

Get the corresponding pygame package

    http://pygame.org/download.shtml

## Run

From the project root

`python ./src/testRun.py`

This will run a test window with one house, person, and idol for each team. The people will attack each other and then the game will end when one dies.

Note that running the script from another directory will cause problems loading the images.

## What works:

   * Creates a simple world with 2 tribes.
   * The people in the tribes can
   * build houses,
   	 * worship at the idol (becoming the tribe leader),
   	 * and fight the other tribe
   * The houses can
      * generate new people
   * The player can
      * start a new game
	    * end the game

## TODO
   * sort out the module/package convention
	  * having read https://docs.python.org/3/tutorial/modules.html I think I need to get rid of the src directory 
	     and refrence other modules from the package root. this should prevent the failures I'm seeingin the unit tests.
   * fix the unit tests.
   * continue refactoring the modules, splitting the classes into their own module files.
   * plan an event driven system 
	  * need to look at pythin events vs pygame events. 
	      * Looks like pygame events are designed for UI and will stop registering events when the queue gets to a certain size.


   * create a landscape
	    * concept of land & water
			* height map
			* generator
  * Houses
    * Need to grow based on the area they have available to them
	* building them needs to take into account the area cultivated by existing houses
	* mark squares as cultivated by specific houses & tribes
	* cannot cultivate sloping areas of the landscape
  * Natives
    * ???
  * Teams
	* How does the power meter grow?
	* Show population meters
  * Interface
	* God powers
		* Move the idol
		* create knight
		* Raise lower land (at the corners)
		* Swamp
		* earthquake
		* Rain of fire
		* volcano
		* flood
		* Armageddon
		* Info icon
	* Team Goal setting
		* build/fight/idol
	* Options
	* save/load games
	* Multiplayer
	* Sounds/music



