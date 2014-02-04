#!/usr/bin/env python
"""
A simple foos client
"""
import socket

NUM_FOOSPLAYERS = 26
NUM_FIELDED = 22
ITER_PER_QUARTER = 200

MAX_MESSAGE_LENGTH = 1024
DELIMITER = ' '

class FoosGame:
  def __init__(self, game_id):
    self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.comm.connect(('crisco.seas.harvard.edu',8080))
    #self.comm.connect(('localhost',8080))
    self.comm.send(game_id)
    data = self.comm.recv(MAX_MESSAGE_LENGTH)
    print "Waiting for game", data
    data = self.comm.recv(MAX_MESSAGE_LENGTH)
    print data
    assert data == "READY"
    self.game_state = [0, 0, 0, 0]

  def __del__(self):
    self.comm.close()


  def is_valid(self, move):
    # Makes sense as a roster
    if len(move) != NUM_FOOSPLAYERS:
      return False

    # Has exactly NUM_FIELDED players on the field
    if sum([abs(p) < 5 for p in move]) != NUM_FIELDED:
      return False

    # If this is a new quarter, then any fielded roster is ok
    if self.game_state[2] % ITER_PER_QUARTER == 0:
      return True

    # Else we're mid-quarter and can only move one player to an adjacent row
    player_pos = self.game_state[4:(4+NUM_FOOSPLAYERS)]
    is_one_moved = (sum([abs(s-p) for (s,p) in zip(player_pos,move)]) <= 1)
    return is_one_moved


  def make_move(self, move):
    # Check if this is a valid move and display a warning
    if not self.is_valid(move):
      print "**WARNING!! SUBMITTING INVALID MOVE**"
    move_string = DELIMITER.join(map(str,move))
    print "Sending: ", move_string
    self.comm.send(move_string)
    message = self.comm.recv(MAX_MESSAGE_LENGTH)
    print "Recieving: ", message
    if not message:
      print "GAME KILLED"
      exit()
    self.game_state = [int(x) for x in message.split(DELIMITER)]
    return self.game_state

