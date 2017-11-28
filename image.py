import cv2
import numpy as np

import scan_functions

class Image(object):
    '''
    image object, most important values are:
    Image.aligned is the sized and aligned image to copy and mark
    Image.scanimg is the properly thresholded version of the image for scanning
    '''
    def __init__(self, fname, scan_settings):
        self.img = cv2.imread(fname, 1)
        self.sz = self.img.shape
        #resize the image
        resizefactor=scan_settings.sz[1]/self.sz[1]
        imgsized = cv2.resize(self.img.copy(), (int(resizefactor*self.sz[1]), int(resizefactor*self.sz[0])), interpolation = cv2.INTER_AREA)
        self.regPts = scan_functions.getRegPts(imgsized, scan_settings)
        # align the image to the fixed coordinates
        self.aligned = scan_functions.imgReg(imgsized, self.regPts, scan_settings)
        # auto thresh the image based on markers
        self.scanimg = scan_functions.autothresh(self.aligned.copy(), scan_settings)
