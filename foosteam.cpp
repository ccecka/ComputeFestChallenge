#include <iostream>
#include <vector>

#include "FoosGame.hpp"

/** Determine a roster for the next round from the current game state.
 * Input:
 * game_state[0]: team score
 * game_state[1]: opponent team score
 * game_state[2]: game round number
 * game_state[3]: row number of the ball
 * game_state[4 ]-[ 29]: team foosplayer row positions
 * game_state[30]-[ 55]: team foosplayer fatigues
 * game_state[56]-[ 81]: opponent foosplayer row positions
 * game_state[81]-[107]: opponent foosplayer fatigues
 * Output:
 * roster[0]-[NUM_FOOSPLAYERS-1]: team foosplayer row positions for next round
 */
std::vector<int> new_move(const std::vector<int>& game_state) {
  // Trivial strategy, null move
  std::vector<int> roster(game_state.begin() + 4,
                          game_state.begin() + 4 + NUM_FOOSPLAYERS);

  return roster;
}


int main(int argc, char** argv)
{
  if (argc != 2) {
    std::cout << "Usage: " << argv[0] << " GAMEID\n\tGAMEID = 0    creates a new game\n\tGAMEID = WXYZ connect to a specific game" << std::endl;
    exit(0);
  }

  // Connect to a FoosGame with id from the command line
  FoosGame game(argv[1]);

  // Initial roster -- defense!
  std::vector<int> roster(NUM_FOOSPLAYERS, -4);
  roster[0] = roster[1] = roster[2] = roster[3] = 100;

  std::vector<int> game_state;
  while (true) {
    // Send the roster and get the game state
    game_state = game.make_move(roster);
    if (game_state[2] == 4 * ITER_PER_QUARTER)
      break;

    // Use the game state to determine the next move
    roster = new_move(game_state);
  }

  std::cout << "Final Score: "
            << game_state[0] << " - " << game_state[1] << std::endl;
  if (game_state[0] > game_state[1])
    std::cout << "WIN!" << std::endl;
  if (game_state[0] == game_state[1])
    std::cout << "Tie Game" << std::endl;

  return 0;
}
