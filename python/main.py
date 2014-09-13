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

  def run(self):
    while(self.cap.isOpened()):
      ret, frame = self.cap.read()
      cv2.imshow('Goats Without Hats!', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if __name__ == '__main__':
  Vision().run()
