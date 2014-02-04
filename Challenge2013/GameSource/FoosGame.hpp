#pragma once

#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <iterator>
#include <assert.h>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

const int NUM_FOOSPLAYERS = 26;
const int NUM_FIELDED = 22;
const int ITER_PER_QUARTER = 200;

const int MAX_MESSAGE_LENGTH = 1024;

class FoosGame
{
  int comm;
  char buffer[1024];
  std::vector<int> game_state;

 public:
  FoosGame(const std::string& game_id) {
    comm = socket(AF_INET, SOCK_STREAM, 0);

    hostent* server = gethostbyname("crisco.seas.harvard.edu");
    if (server == NULL) {
      printf("No such host!\n");
    }

    sockaddr_in serv_addr;
    bzero((char*) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);
    bcopy((char *)server->h_addr,
          (char *)&serv_addr.sin_addr.s_addr,
          server->h_length);

    if (connect(comm, (sockaddr*) &serv_addr, sizeof(serv_addr)) < 0)
      printf("Error\n");

    if (write(comm, game_id.c_str(), game_id.size()) == -1) {
      printf("Write error\n");
    }

    bzero(buffer, 1024);
    if (read(comm, buffer, 1024) == -1) {
      printf("Read error\n");
    }

    printf("Waiting for game %s\n", buffer);

    int read_char = read(comm, buffer, 1023);
    std::string message(buffer, read_char);

    std::cout << message << std::endl;
    assert(message == std::string("READY"));

    // Dummy game state [0,0,0,0] for now
    game_state = std::vector<int>(4, 0);
  }

  ~FoosGame() {
    close(comm);
  }

  bool is_valid(const std::vector<int>& move) {
    // Makes sense as a roster
    if (move.size() != NUM_FOOSPLAYERS)
      return false;

    // Has exactly NUM_FIELDED players on the field
    int num_fielded = 0;
    for (int i = 0; i < NUM_FOOSPLAYERS; ++i)
      if (abs(move[i]) <= 4)
        ++num_fielded;
    if (num_fielded != NUM_FIELDED)
      return false;

    // If this is a new quarter, then any fielded roster is ok
    if (game_state[2] % ITER_PER_QUARTER == 0)
      return true;

    // Else we're mid-quarter and can only move one player to an adjacent row
    int num_moved = 0;
    for (int i = 0; i < NUM_FOOSPLAYERS; ++i)
      num_moved += abs(move[i] - game_state[i+4]);

    return num_moved <= 1;
  }

  std::vector<int> make_move(const std::vector<int>& move) {
    if (!is_valid(move)) {
      std::cout << "**WARNING!! SUBMITTING INVALID MOVE" << std::endl;
    }

    std::stringstream ss;
    std::copy(move.begin(), move.end(), std::ostream_iterator<int>(ss, " "));
    std::string move_string = ss.str();

    std::cout << "Sending: " << move_string << std::endl;
    int write_char = write(comm, move_string.c_str(), move_string.size());


    int read_char = read(comm, buffer, 1023);
    if (read_char == -1)
      std::cout << "ERROR" << std::endl;
    std::string message(buffer, read_char);
    std::cout << "Recieving: " << message << std::endl;

    if (message == std::string("")) {
      std::cout << "GAME KILLED" << std::endl;
      exit(0);
    }

    game_state.clear();
    std::stringstream msgstream(message);
    std::copy(std::istream_iterator<int>(msgstream), std::istream_iterator<int>(),
              std::back_inserter(game_state));
    return game_state;
  }
};
