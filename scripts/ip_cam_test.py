import base64
import time
import urllib2

import cv2
import numpy as np


"""
Examples of objects for image frame aquisition from both IP and
physically connected cameras
Requires:
 - opencv (cv2 bindings)
 - numpy
"""


class ipCamera(object):

    def __init__(self="http://192.168.86.35/mjpeg.cgi", user="admin", password="supple123"):
        self.url = url
        auth_encoded = base64.encodestring('%s:%s' % (user, password))[:-1]

        self.req = urllib2.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def get_frame(self):
        response = urllib2.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame


class Camera(object):

    def __init__(self, camera=0):
        self.cam = cv2.VideoCapture(camera)
        if not self.cam:
            raise Exception("Camera not accessible")

        self.shape = self.get_frame().shape

    def get_frame(self):
        _, frame = self.cam.read()
        return frame