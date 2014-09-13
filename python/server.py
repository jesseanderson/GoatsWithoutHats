import socket
import threading

class server(object):
  def __init__(self, getSound, newPlayer, **kwargs):
    super(server,self);
    self.s = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 50000
    self.s.bind((HOST, PORT))

    #List of client sockets
    #Tuples of socket, address, and color
    self.clients = []

    #OpenCV interface
    self.getSound = getSound
    self.newPlayer = newPlayer

  def main(self):
    self.s.listen(5)
    #Listen in new thread to not block other operations
    cThread = threading.Thread(target = self.getClients)
    cThread.setDaemon(True)
    cThread.start()

    while(True):
      #Implement delay for loop; we don't update every time

      #Use client list to get position data from OpenCV
      #TransferData: list of socket, data to send to it
      transferData = self.getData()

      #Transfer the locations to clients
      self.sendData(transferData)

  #May want another thread for this to deal with accept
  def getClients(self):
    #Loop until we find no more sockets
    while(True):
        client, addr = self.s.accept()
        data = client.recv(1)

        #Inform OpenCV of the new player
        self.newPlayer(data)
        self.clients.append((client, addr, data))

  def getData(self):
    #Interface with OpenCV to compute list of client
    #information
    data = []
    for client in self.clients:
        #Red = 0, Blue = 1, Orange = 2
        color = client[2]
        #Value 0-9; issues exist with sending different
        #sized strings.
        distance = self.getSound(color)
        information = (client[0], client[1], distance)
        data.append(information)
    return data

  def sendData(self, transferData):
    #Go through our clients and send them their data
    for client in transferData:
      clientSock = client[0]
      data = client[2]

      clientSock.send(data)