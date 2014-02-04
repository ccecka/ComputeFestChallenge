TODO:
	Time limit?
	Online visualizer?

Using a communication portal allows the students to use any language they like and makes it nearly trivial to pit students' solutions against each other (especially inter-language):

To launch the host server:

  python FoosHost.py

This server is responsible for listening to connections from players, creating games, and launching games once enough players have joined a game.

To launch a player (use 'localhost' in FoosArena.py for local testing, we'll use 'crisco.seas.harvard.edu' for a dedicated server during the competition):

  python foosteam.py 0

The 0 command-line argument tells the server to generate a random game ID. We could also provide our own. The server respondes with the game ID and the team outputs:

  Waiting for game ####   (say... 7842)

To join this game, another team can be launched with this game ID:

  python foosteam 7842

The server responds to both teams with "READY" and the game loop is entered within each team. If there is an error server-side or client-side the players are disconnected and the game is closed.
