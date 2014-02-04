#!/usr/bin/env python
import sys

import FoosGame

NUM_FOOSPLAYERS = 26
NUM_FIELDED = 22
ITER_PER_QUARTER = 200

def new_move(game_state):
  """Determine a roster for the next round from the current game state.
  Input:
  game_state[0]: team score
  game_state[1]: opponent team score
  game_state[2]: game round number
  game_state[3]: row number of the ball
  game_state[ 4:30 ]: team foosplayer row positions
  game_state[30:56 ]: team foosplayer fatigues
  game_state[56:82 ]: opponent foosplayer row positions
  game_state[82:108]: opponent foosplayer fatigues
  Output:
  move[0:NUM_FOOSPLAYERS]: team foosplayer row positions for next round
  """
  # Trivial strategy, null move
  return game_state[4:(4+NUM_FOOSPLAYERS)]



if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "Usage: python", sys.argv[0], "GAMEID\n\tGAMEID = 0    creates a new game\n\tGAMEID = WXYZ connect to a specific game"
    exit()

  # Connect to a FoosGame with id from the command line
  game = FoosGame.FoosGame(sys.argv[1])

  # Initial roster - defense!
  roster = [-4] * NUM_FOOSPLAYERS
  roster[0:4] = [100,100,100,100]

  while True:
    # Send the roster and get the game state
    game_state = game.make_move(roster)
    if game_state[2] == 4 * ITER_PER_QUARTER:
      break

    # Use the game state to determine the next move
    roster = new_move(game_state)

  print "Final Score:", game_state[0], "-", game_state[1]
  if game_state[0] > game_state[1]:
    print "WIN!"
  if game_state[0] == game_state[1]:
    print "Tie Game"
