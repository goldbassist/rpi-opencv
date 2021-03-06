#!/usr/bin/env python

"""color-3.py: Color (white HSV range) detection using openCV."""

""" Performance: on video (mp4 sample) and running in a RMBP -> 0.03s each detection or 33hz """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import cv2, math
import numpy as np
import time

class ColorTracker:
  def __init__(self):
    cv2.namedWindow("ColorTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
    self.capture = cv2.VideoCapture(0)
    #self.capture = cv2.VideoCapture('crash-480.mp4')
    self.capture.set(3,640)
    self.capture.set(4,480)
    self.scale_down = 4
  def run(self):
    while True:
      t1 = time.time()

      f, orig_img = self.capture.read()
      orig_img = cv2.flip(orig_img, 1)
      img = cv2.GaussianBlur(orig_img, (5,5), 0)
      img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
      img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))

      # Blue
      #color = cv2.inRange(img,np.array([100,50,50]),np.array([140,255,255]))

      # Green
      #color = cv2.inRange(img,np.array([40,50,50]),np.array([80,255,255]))

      # Red
      color = cv2.inRange(img,np.array([0,150,0]),np.array([5,255,255]))

      # White
      #sensitivity = 10
      #color = cv2.inRange(img,np.array([0,0,255-sensitivity]),np.array([255,sensitivity,255]))

      binary = color
      dilation = np.ones((15, 15), "uint8")
      binary = cv2.dilate(binary, dilation)
      contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      max_area = 0
      largest_contour = None
      for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
          max_area = area
          largest_contour = contour
      if largest_contour is not None:
        moment = cv2.moments(largest_contour)
        if moment["m00"] > 1000 / self.scale_down:
          rect = cv2.minAreaRect(largest_contour)
          rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
          box = cv2.cv.BoxPoints(rect)
          box = np.int0(box)
          cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)

          x = rect[0][0]
          y = rect[0][1]
          t2 = time.time()
          print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)
          cv2.imshow("ColorTrackerWindow", orig_img)
          
          if cv2.waitKey(20) == 27:
            cv2.destroyWindow("ColorTrackerWindow")
            self.capture.release()
            break
      else:
        cv2.imshow("ColorTrackerWindow", orig_img)

if __name__ == "__main__":
  color_tracker = ColorTracker()
  color_tracker.run()