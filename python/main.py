import sys
import numpy as np
import cv2

"""Global Constants go here in CAPS"""

class Vision(object):
  def __init__(self, **kwargs):
    super(Vision, self).__init__(**kwargs)
    if(len(sys.argv) > 1): #Video File input
      self.cap = cv2.VideoCapture(str(sys.argv[1]))
    else: #Webcam input
      self.cap = cv2.VideoCapture(0)
    self.players = []

  def run(self):
    while(self.cap.isOpened()):
      ret, frame = self.cap.read()
      cv2.imshow('Goats Without Hats!', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    self.cap.release()
    cv2.destroyAllWindows()

class Game(object):

  def __init__(self, **kwargs):
    super(Game, self).__init__(**kwargs)
    self.players = []
    self.vision = Vision()

  def run(self):
    self.vision.run()
    
  def add_player(self, color):
    pass

  def send_status(self, color):
    pass

if __name__ == '__main__':
  Game().run()
