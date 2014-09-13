import sys
import numpy as np
import random
import cv2
from server import server

"""Global Constants go here in CAPS"""

class Vision(object):
  def __init__(self, **kwargs):
    super(Vision, self).__init__(**kwargs)
    if(len(sys.argv) > 1): #Video File input
      self.cap = cv2.VideoCapture(str(sys.argv[1]))
    else: #Webcam input
      self.cap = cv2.VideoCapture(0)
    self.tracking = []
    self.previous_locs = []
    self.animal_locs = []
    self.width = self.cap.get(3)
    self.height = self.cap.get(4)

  def run(self):
    while(self.cap.isOpened()):
      ret, frame = self.cap.read()

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
          thresh = cv2.inRange(hsv_frame, lower_color, upper_color)
          _, contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
          max_area = 0
          best_cnt = 1
          for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
              max_area = area
              best_cnt = cnt
          if best_cnt is 1:
            cx, cy = self.previous_locs[player]
          else:
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            self.previous_locs[player] = (cx, cy)
          cv2.circle(frame,(cx,cy),5,255,-1)
          """FUTURE ANIMAL CRAP"""
          cv2.circle(frame,self.animal_locs[player],5,255,-1)
      """End Tracking"""
      cv2.imshow('Goats Without Hats!', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    self.cap.release()
    cv2.destroyAllWindows()

  def start_tracking(self, color, player):
    self.tracking.append((color, player))
    self.previous_locs.append((0,0))

class Game(object):

  def __init__(self, **kwargs):
    super(Game, self).__init__(**kwargs)
    self.players = []
    self.player_count = 0
    self.animals = []
    self.vision = Vision()
    self.server = server(self.send_status, self.add_player, self.remove_player)
    self.server.main()
    self.add_player(1)

  def run(self):
    self.vision.run()
    
  def add_player(self, color):
    self.vision.start_tracking(color, self.player_count)
    self.vision.previous_locs.append((0,0))
    self.player_count = self.player_count + 1
    animal_x = 0
    animal_y = 0
    while(animal_x == 0 and animal_y == 0):
      animal_x = int(random.random() * self.vision.width)
      animal_y = int(random.random() * self.vision.height)
    self.animals.append((animal_x, animal_y))
    self.vision.animal_locs.append((animal_x, animal_y))

  def remove_player(self, color):
    pass

  def send_status(self, color):
    #VARIABLES TO CHANGE TO DETERMINE CORRECT VALUES
    radius_ratio = .7
    win_ring_radius = 10
    WIN_SOUND = 9
    ################################################
    #Find the player
    for p in self.players:
      if(p[0] == color):
        player_id = p[1]
        break

    pX, pY = self.vision.previous_locs[player_id]
    aX, aY = self.vision.animal_locs[player_id]
    h, w = self.vision.height, self.vision.width
    radius = radius_ratio * (max(h,w)/2) - win_ring_radius
    ring_size = radius / 9

    dist = (((aX - pX)**2) + ((aY - pY)**2))**.5
    #Check for win ring
    if(dist < win_ring_radius):
      return WIN_SOUND

    #Shift towards center
    dist -= win_ring_radius

    sound_level = dist / ring_size

    return 9 - sound_level

if __name__ == '__main__':
  Game().run()
