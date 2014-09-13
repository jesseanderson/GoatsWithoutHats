class server(object):
  def __init__():
    super(self,server);
    self.s = socket.socket(socket.AF_INET,
                                socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 50000
    s.bind((HOST, PORT))

    #List of client sockets
    #Tuples of socket, address, and color
    self.clients = []

    s.listen(5)
    while(True):
      self.main()

  def main(self):
    #Be aware of either timeout or threading needs
    #Connect clients and put them in list
    self.getClients()

    #Use client list to get position data from OpenCV
    #TransferData: list of socket, data to send to it
    transferData = self.getData()

    #Transfer the locations to clients
    self.sendData(transferData)

  def getClients(self):
    #Loop until we find no more sockets
    pass

  def getData(self):
    #Interface with OpenCV to compute list of client
    #information
    pass

  def sendData(self, transferData):
    #Go through our clients and send them their data
    pass

