class server(object):
  def __init__(self, **kwargs, getSound, newPlayer):
    super(self,server);
    self.s = socket.socket(socket.AF_INET,
                                socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 50000
    s.bind((HOST, PORT))

    #List of client sockets
    #Tuples of socket, address, and color
    self.clients = []

    #OpenCV interface
    self.getSound = getSound
    self.newPlayer = newPlayer

  def main(self):
    self.s.listen(5)
    #############START IN NEW THREAD###############
    self.getClients()
    ###############################################
    while(True):
      #Be aware of either timeout or threading needs
      #Connect clients and put them in list
      

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
        data = client.recv(1024)
        self.clients.append((client, addr, data))

  def getData(self):
    #Interface with OpenCV to compute list of client
    #information
    num = len(self.clients)
    data = []
    for i in num:
        color = self.clients[i][2]
        distance = self.getSound(color)
        information = (self.clients[i][0], self.clients[i][1], distance)
        data.append(information)
    return (data)

  def sendData(self, transferData):
    
    #Go through our clients and send them their data
    for client in transferData:
      clientSock = client[0]
      data = client[1]
      clientSock.send(data)
