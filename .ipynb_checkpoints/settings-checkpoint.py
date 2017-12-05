import cv2
import numpy as np

class Settings():
    '''
    A class to store all the settings for pyExamScan_v2
    '''
    def __init__(self):
        '''Initialize the settings'''
        # set a threshold for finding registration marks
        self.volthresh = 180
        # set some factors for image registration/alignement
        self.warp_mode = cv2.MOTION_EUCLIDEAN
        self.number_of_iterations = 50;
        self.termination_eps = 1e-10;
        self.criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                            self.number_of_iterations, 
                            self.termination_eps
                            )

        # set the kernel size for erosion/dilation
        self.kern=np.ones((4,4),np.int8)
        # set the document size (#rows, #columns) to work with. All images will be scaled to this size
        self.sz = (1584, 1224)
        # set the coordinates for the registration points
        self.keyRegPts = np.array([[1153, 1532], [73, 1532],  [1153, 64]], dtype = np.float32)
        #set locations for threshold cues
        threshdict={}
        threshdict['thresh01']=(607,55),(635,83)
        threshdict['thresh02']=(600,1520),(626,1548)
        threshdict['thresh03']=(36,828),(68,856)
        threshdict['thresh04']=(1165,842),(1193,870)
        self.threshdict = threshdict
        #set the relative threshold value for threshdict
        self.sigma = 0.25
