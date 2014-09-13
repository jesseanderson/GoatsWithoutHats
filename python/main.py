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
    self.tracking = [(1,0)]

  def run(self):
    while(self.cap.isOpened()):
      ret, frame = self.cap.read()
      cv2.imshow('Goats Without Hats!', frame)
      """Start Tracking"""
      if self.tracking:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for color, player in self.tracking:
          if color == 0: #RED
            lower_color = np.array([0,50,50])
            upper_color = np.array([20,255,255])
          elif color == 1: #BLUE
            lower_color = np.array([110,50,50])
            upper_color = np.array([130,255,255])
          elif color == 2: #ORANGE
            lower_color = np.array([30,50,50])
            upper_color = np.array([50,255,255])
          mask = cv2.inRange(hsv_frame, lower_color, upper_color)
          res = cv2.bitwise_and(frame, frame, mask= mask)
          
      """End Tracking"""
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    self.cap.release()
    cv2.destroyAllWindows()

  def start_tracking(self, color, player):
    self.trackin

class Game(object):

  def __init__(self, **kwargs):
    super(Game, self).__init__(**kwargs)
    self.players = []
    self.player_count = 0
    self.vision = Vision()

  def run(self):
    self.vision.run()
    
  def add_player(self, color):
    self.vision.start_tracking(color, self.player_count)
    self.player_count = self.player_count + 1

  def send_status(self, color):
    pass

if __name__ == '__main__':
  Game().run()
