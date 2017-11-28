import numpy as np
import cv2
import pandas as pd
import fnmatch

    
def getid(idRes, nRes):
    #compile student name
    lastName=nRes['N1']+nRes['N2']+nRes['N3']+nRes['N4']+nRes['N5']
    firstName=nRes['F1']+nRes['F2']+nRes['F3']
    #get list of ID keys
    studentID = ''
    for k, v in sorted(idRes.items()):
        studentID = studentID + str(v)    
    return lastName, firstName, studentID

    
    
'''stuff left over from old scanDots
    
    # Stuff for marking the images
                            #if it's not the key
                        if not self.key:
                            #check to see if that value is in the key for that question
                            if lett not in self.keyDict[k]:
                                #mark it as wrong
                                #get x and y coordinates as coord + starting point from areaDict
                                markX=self.areaDict[k][0][0]+coord-8
                                markY=self.areaDict[k][1][1]
                                #mark an X on self.img2orig which has been aligned
                                cv2.putText(self.img2orig, 'X',
                                    (markX, markY),
                                    cv2.FONT_HERSHEY_SIMPLEX,1,
                                    (0,0,255), 2)
                            #mark it as correct
                            if lett in self.keyDict[k]:
                                #get x and y coordinates as coord + starting point from areaDict
                                markX=self.areaDict[k][0][0]+coord-8
                                markY=self.areaDict[k][1][1]
                                #put a green C on self.img2orig which has been aligned
                                cv2.putText(self.img2orig, 'C',
                                    (markX, markY),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0,255,0), 2)
                                    
                                    
                                    # now need to mark missing answers
        if self.markmissing and not self.key and k[0]=='Q':
            #set a boolean operator
            M=False
            #check to see if values in key are not on answer sheet
            for keyAns in self.keyDict[k]:
                # if the correct answer is nothing, or if we already found a missing answer, no need to mark again
                if keyAns == '-' or M:
                    break
                # if one of the correct answers is missing from the students sheet
                if keyAns not in self.resDict[k]:
                    #put a red "M" over question number to mark as "missing"
                    markX=self.areaDict[k][0][0]-25
                    markY=self.areaDict[k][1][1]
                    cv2.putText(self.img2orig, 'M',
                            (markX, markY),
                            cv2.FONT_HERSHEY_SIMPLEX,1,
                            (0,0,255), 2)
                    #and if we put an M, go on to the next question so we don't put multiple M's on top of each other
                    M=True
'''