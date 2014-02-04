

class foosteam
{
  public static int NUM_FOOSPLAYERS = 26;
  public static int NUM_FIELDED = 22;
  public static int ITER_PER_QUARTER = 200;

  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Usage: java foosteam GAMEID"
                         + "\n\tGAMEID = 0    creates a new game"
                         + "\n\tGAMEID = WXYZ connect to a specific game");
      return;
    }

    // Connect to a FoosGame with id from the command line
    FoosGame game = new FoosGame(args[0]);

    // Initial roster -- defense!
    int[] roster = {100, 100, 100, 100,
                    -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4,
                    -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4};

    int[] game_state;
    while (true) {
      // Send the roster and get the game state
      game_state = game.make_move(roster);
      if (game_state[2] == 4 * ITER_PER_QUARTER)
        break;

      // Use the game state to determine the next move
      roster = new_move(game_state);
    }

    System.out.println("Final Score: " + game_state[0] + " - " + game_state[1]);
    if (game_state[0] > game_state[1])
      System.out.println("WIN!");
    if (game_state[0] == game_state[1])
      System.out.println("Tie Game");
  }


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
  public static int[] new_move(int[] game_state) {
    // Trivial strategy, null move
    int[] roster = new int[NUM_FOOSPLAYERS];
    for (int i = 0; i < NUM_FOOSPLAYERS; ++i) {
      roster[i] = game_state[i+4];
    }
    return roster;
  }


}
