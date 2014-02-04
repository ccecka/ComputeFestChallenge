import asyncore
import random
import collections
import socket

import FoosGameEngine

MAX_MESSAGE_LENGTH = 1024

class RemoteClient(asyncore.dispatcher):
  """Wraps a remote client socket."""

  def __init__(self, host, socket, address):
    asyncore.dispatcher.__init__(self, socket)
    self.host = host
    self.address = address
    self.game_id = None

  def handle_read(self):
    message = self.recv(MAX_MESSAGE_LENGTH).strip()
    #print 'Recieved from', self.address, ": ", message
    if message:
      self.host.handle_message(self, message)

  def handle_close(self):
    self.host.remove_client(self)

  def write(self, message):
    #print "Sending to", self.address, ": ", message
    if len(message) > MAX_MESSAGE_LENGTH:
      raise ValueError('Message too long')
    self.send(message)

class Host(asyncore.dispatcher):
  """Wraps a host socket listens for players and creates games"""

  def __init__(self, address=('', 8080)):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(address)
    self.listen(5)
    self.remote_clients = []
    self.game = {}

  def handle_accept(self):
    socket, addr = self.accept()
    print 'Accepted', addr
    self.remote_clients.append(RemoteClient(self, socket, addr))
    print 'Total clients:', len(self.remote_clients)

  def remove_client(self, client):
    # If this client does not have a game, just close and return
    if client.game_id == None:
      print "Closing", client.address
      client.close()
      self.remote_clients.remove(client)
      return

    # Remove all the players of the game this client is in
    for player in self.game[client.game_id].players():
      if player != None:
        print "Closing", player.address
        player.close()
        self.remote_clients.remove(player)
    # Remove the game this client was in
    print "Closing game", client.game_id
    del self.game[client.game_id]
    print 'Total clients:', len(self.remote_clients)
    print 'Total games:', len(self.game)

  def handle_message(self, client, message):
    if client.game_id == None:
      client.game_id = message    # Set the new game key
      if client.game_id == "0":   # Create a new game with random key
        client.game_id = str(random.randint(1000,10000))
      # Echo the game ID to the client
      client.write(client.game_id)

      # If this game doesn't exist, create it
      if not client.game_id in self.game:
        print "Creating game", client.game_id
        self.game[client.game_id] = FoosGameEngine.FoosGame()
        print 'Total games:', len(self.game)
      # Attempt to add the client to the game
      if not self.game[client.game_id].add_player(client):
        client.write("Error: Player was not added to game")
        client.close()
        self.remote_clients.remove(client)
      # If the game is ready, notify the players
      if self.game[client.game_id].is_ready():
        print "Starting game", client.game_id
        for player in self.game[client.game_id].players():
          player.write("READY")
    else:
      # Active game, let the game engine interprit the move
      self.game[client.game_id].make_move(client, message)


if __name__ == '__main__':
  print "Creating host"
  host = Host()
  print "Listening..."
  asyncore.loop()


