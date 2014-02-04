import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;

class FoosGame
{
  private Socket comm;
  private DataInputStream in;
  private DataOutputStream out;

  private byte[] buffer;

  private int[] game_state;

  private static String DELIMITER = new String(" ");
  public static int NUM_FOOSPLAYERS = 26;
  public static int NUM_FIELDED = 22;
  public static int ITER_PER_QUARTER = 200;

  FoosGame(String game_id) {
    try {
      comm = new Socket("crisco.seas.harvard.edu", 8080);
      out = new DataOutputStream(comm.getOutputStream());
      in = new DataInputStream(comm.getInputStream());

      out.write(game_id.getBytes(), 0, game_id.length());

      buffer = new byte[1024];
      in.read(buffer);
      System.out.println("Waiting for game " + new String(buffer));

      Arrays.fill(buffer, (byte) 0);
      in.read(buffer);
      String message = new String(buffer);
      System.out.println(message);

      if (message.equals("READY"))
        System.exit(0);

    } catch(Exception e) {
      System.out.println("ERROR");
    }

    game_state = new int[4];
  }

  public boolean is_valid(int[] move) {
    // Makes sense as a roster
    if (move.length != NUM_FOOSPLAYERS)
      return false;

    // Has exactly NUM_FIELDED players on the field
    int num_fielded = 0;
    for (int i = 0; i < move.length; ++i)
      if (Math.abs(move[i]) <= 4)
        ++num_fielded;
    if (num_fielded != NUM_FIELDED)
      return false;

    // If this is a new quarter, then any fielded roster is ok
    if (game_state[2] % ITER_PER_QUARTER == 0)
      return true;

    // Else we're mid-quarter and can only move one player to an adjacent row
    int num_moved = 0;
    for (int i = 4; i < 4+NUM_FOOSPLAYERS; ++i)
      num_moved += Math.abs(move[i] - game_state[4+i]);

    return num_moved <= 1;
  }

  public int[] make_move(int[] move) {
    // Check is_valid
    try {
      String move_string = array2string(move);
      System.out.println("Sending: " + move_string);
      out.write(move_string.getBytes(), 0, move_string.length());

      Arrays.fill(buffer, (byte) 0);
      in.read(buffer);
      String message = new String(buffer);
      System.out.println("Recieving: " + message);

      if (message.equals("")) {
        System.out.println("GAME KILLED");
        System.exit(0);
      }
      game_state = string2array(message);
    } catch(Exception e) {}

    return game_state;
  }


  public String array2string(int[] array) {
    String temp = Arrays.toString(array).replace(", ", DELIMITER);
    return temp.substring(1, temp.length()-1);
  }

  public int[] string2array(String string) {
    String[] items = string.split(DELIMITER);
    int[] results = new int[items.length];

    for (int i = 0; i < items.length; i++) {
      try {
        results[i] = Integer.parseInt(items[i]);
      } catch (NumberFormatException nfe) {};
    }
    return results;
  }
}
