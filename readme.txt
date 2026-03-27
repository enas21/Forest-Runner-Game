The Python 3.10 Pygame Zero 2D runner platformer game Forest Runner features gameplay where players control a character 
who can move left and right while jumping to collect coins and stay alive until reaching the target score. 

Used Libraries:
	Pygame Zero → main framework for the game 
	pygame.Rect → for collision detection


The game features a main menu system together with animated player and enemy sprites while background music and sound effects create 
sound effects for both winning and losing outcomes. 

The project uses Pygame Zero as its primary development framework while all code executes through Python programming language.
The code also uses the Rect class from Pygame for collision handling. 
The project functions properly without needing any additional external libraries. 

The game requires Python 3.10 to function correctly. The project requires Python 3.10 because I tested it with other versions and it had errors with that. 
so with 3.10 version and I use the command "py -3.10 -m pgzero Main.py" to ensure the correct Python version runs my project.

Make sure that your computer has Python 3.10 installed before you run the project and that Pygame Zero exists in that Python installation. 
All game files must be in the correct project folder which needs to include Main.py and the images folder and the sounds folder and the music files used by the game. 
The asset filenames must exactly match the names which the code uses to refer to them.

The player begins to play the game after the main menu appears on the screen. The menu provides buttons which players can click to begin the game, 
toggle audio settings, and leave the game. The player uses arrow keys to navigate through the game world while using space bar to perform jumps. 
The player must gather 5 coins to achieve the target score while keeping away from enemies. 

The game presents a winning screen to the player after they have collected 5 coins to win the game. 
The game displays the game over screen when the player fails to maintain it's lives.

The project follows an object-oriented design approach. 
The project contains distinct classes which handle animated sprites and player character and enemy character and coin object animations. 
The classes contain movement and animation control systems which enable developers to maintain organized and understandable programming code. 

The player character and enemies show both stationary and active movement animations throughout the game while sound effects exist for all collision events 
and coin collection activities and victory and defeat scenes.

