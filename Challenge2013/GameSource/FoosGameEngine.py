import math
import random

NUM_FOOSPLAYERS = 26
NUM_FIELDED = 22
ITER_PER_QUARTER = 200

MAX_MESSAGE_LENGTH = 1024
DELIMITER = ' '

def list2string(mylist):
  # Make a string
  return DELIMITER.join(map(str,mylist))

def string2list(mystring):
  # Split and cast to ints
  return [int(x) for x in mystring.split(DELIMITER)]


class FoosGame:
  def __init__(self):
    self.player1 = None
    self.player2 = None
    self.p1score = 0
    self.p2score = 0
    self.iter = 0
    self.ball = 0
    self.p1pos = [5] * NUM_FOOSPLAYERS
    self.p1fat = [0] * NUM_FOOSPLAYERS
    self.p2pos = [5] * NUM_FOOSPLAYERS
    self.p2fat = [0] * NUM_FOOSPLAYERS
    self.player1moved = False
    self.player2moved = False

  def is_ready(self):
    return self.player1 != None and self.player2 != None

  def add_player(self, player):
    if self.player1 == None:
      self.player1 = player
      return True
    elif self.player2 == None:
      self.player2 = player
      return True
    else:
      return False

  def players(self):
    return [self.player1, self.player2]


  def is_valid(self, state, move):
    # Makes sense as a roster
    if len(move) != NUM_FOOSPLAYERS:
      return False

    # Has exactly NUM_FIELDED players on the field
    if sum([abs(p) < 5 for p in move]) != NUM_FIELDED:
      return False

    # If this is a new quarter, then any fielded roster is ok
    if self.iter % ITER_PER_QUARTER == 0:
      return True

    # Else we're mid-quarter and can only move one player to an adjacent row
    is_one_moved = (sum([abs(s-p) for (s,p) in zip(state,move)]) <= 1)
    return is_one_moved


  def make_move(self, player, move):
    if player == self.player1 and not self.player1moved:
      # Update the old state by fatiguing players
      for i,x in enumerate(self.p1pos):
        if x == self.ball:
          self.p1fat[i] += 1

      try:
        # If valid, update the state with the move
        move_state = string2list(move)
        if self.is_valid(self.p1pos, move_state):
          self.p1pos = move_state
      except:
        print "MOVE UPDATE ERROR"

      self.player1moved = True
    elif player == self.player2 and not self.player2moved:
      # Update the old state by fatiguing players
      for i,x in enumerate(self.p2pos):
        if x == self.ball:
          self.p2fat[i] += 1

      try:
        # If valid, update the state with the move
        move_state = string2list(move)
        move_state = [-x for x in move_state]
        if self.is_valid(self.p2pos, move_state):
          self.p2pos = move_state
      except:
        print "MOVE UPDATE ERROR"

      self.player2moved = True
    else:
      return    # Shouldn't happen...

    if self.player1moved and self.player2moved:
      # If this is a new quarter, set the benched player fatigues to 0
      if self.iter % ITER_PER_QUARTER == 0:
        for i,x in enumerate(self.p1pos):
          if abs(x) > 4:
            self.p1fat[i] = 0
        for i,x in enumerate(self.p2pos):
          if abs(x) > 4:
            self.p2fat[i] = 0

      # Compute the team strengths on the ball row
      p1strength = sum([math.pow(0.99,e) for i,e in enumerate(self.p1fat)
                        if self.p1pos[i] == self.ball])
      p2strength = sum([math.pow(0.99,e) for i,e in enumerate(self.p2fat)
                        if self.p2pos[i] == self.ball])
      if p1strength + p2strength == 0:
        R = 0.5
      else:
        R = p1strength / (p1strength + p2strength)

      # Increment the ball
      r = random.random()
      if r < R:
        self.ball += 1
      elif r > R:
        self.ball -= 1

      # Detect goals
      if self.ball > 4:
        self.p1score += 1
        self.ball = 0
      if self.ball < -4:
        self.p2score += 1
        self.ball = 0

      # Increament the iteration
      self.iter += 1

      # If this is a new quarter, set the ball to midfield
      if self.iter % ITER_PER_QUARTER == 0:
        self.ball = 0

      # Send state to the players
      self.player1.write(list2string(
          [self.p1score, self.p2score, self.iter, self.ball]
          + self.p1pos + self.p1fat
          + self.p2pos + self.p2fat))
      self.player2.write(list2string(
          [self.p2score, self.p1score, self.iter, -self.ball]
          + [-x for x in self.p2pos] + self.p2fat
          + [-x for x in self.p1pos] + self.p1fat))

      # If the game is over
      if self.iter == 4 * ITER_PER_QUARTER:
        self.player1.handle_close()

      # Open for the next moves
      self.player1moved = False
      self.player2moved = False
