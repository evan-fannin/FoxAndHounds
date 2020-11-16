Hello there.

This is a guide to running this project.

First and foremost, you're going to need a virtual environment! Aside from the dependencies used for
our original homework project, you're going to need the package networkx.
The easiest way to get everything is to use pipenv. If you don't have it, install pipenv.
Then set up a virtual environment in PyCharm, selecting the pipenv environment option.
If PyCharm doesn't install dependencies from this project's Pipfile automatically,
just type "pipenv install" in the PyCharm terminal. Then you'll be good to go!

If you would like to see the results of several different setups that were already played through, simply peruse
through the 8 games already logged in logfile.txt.

If you would like to play a game yourself, simply run demo.py and type in your choice of observation or active participation as
one of the players.

Would you like to play from a setup that isn't the default one? Can do, just go to
line 544 in games.py. Comment out line 544 and uncomment the section directly below it.
Then you can alter that game board that you just uncommented and that will be your initial setup
when you run demo.py to play the game.

Have fun. But not too much fun, okay?