import numpy as np
import cv2
import fnmatch

#def loadandalign(fname):
#    img = Image(fname)
    
    
def imgReg(img, regPts, scan_settings):
    '''
    align image with registration coordinates
    '''
    #create the transformation matrix 
    warp_matrix = cv2.getAffineTransform(scan_settings.keyRegPts,regPts)
    #align the image
    img_aligned = cv2.warpAffine(img, warp_matrix, (scan_settings.sz[1],scan_settings.sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return img_aligned

def getRegPts(img, scan_settings): 
    '''
    find the three registration points and return the sorted array
    '''
    # blur, convert to b&w, threshold image (which has already been resized)
    bw=cv2.medianBlur(img, 7)
    bw=cv2.cvtColor(bw,cv2.COLOR_BGR2GRAY)
    ret, imgthresh = cv2.threshold(bw.copy(), scan_settings.volthresh, 255, cv2.THRESH_BINARY_INV)
    
    # find contours
    (_, cnts, _) = cv2.findContours(imgcopy,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #get the contours sorted by size
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    # initiate the alignment points list
    pts=[]
    for c in cnts:
        (x, y, w, h)=cv2.boundingRect(c)
        #if the contour is not basically a square, ignore it
        if w/h > 1.2 or w/h <.833:
            continue
        #if the contour varies too much from the expected area (which is 1384 pixels) ignore it
        if (cv2.contourArea(c) > int(scan_settings.sz[1] * 1.2) or 
                cv2.contourArea(c) < int(scan_settings.sz[1] * 0.8)):
            continue
        #get the center of each dot and add the centers to pts variable
        M=cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        pts.append((cX,cY))
        if len(pts)==3:
            break
    # need sorted pnts to be bottom right, bottom left, top right
    # so find which pts is the bottom right
    # which will be the maximum of the sum of the x and y coords of each point
    bridx=np.argmax([sum(tup) for tup in pts])
    br=pts[bridx]
    #remove that point from the list
    del pts[bridx]
    #of the remaining pnts, bottom left will be the one with the smallest x-coord
    bl=sorted(pts)[0]
    #and top right will be the one with the smallest y-coord
    tr=sorted(pts)[1]
    #rewrite pts so it's sorted properly
    pts=[br, bl, tr]
    #return pts in the format needed for the warp operations
    return np.array(pts,dtype=np.float32)
    
def autothresh(aligned_img, scan_settings):
    img=cv2.cvtColor(aligned_img.copy(),cv2.COLOR_BGR2GRAY)
    img=cv2.medianBlur(img, 15)
    threshdict=scan_settings.threshdict
    threshvals = np.full((4,1),np.nan)
    for j in range(1,5):
        keyName = 'thresh' + format(j,'02d')
        startX=threshdict[keyName][0][0]
        endX=threshdict[keyName][1][0]
        startY=threshdict[keyName][0][1]
        endY=threshdict[keyName][1][1]
        pt1 = startX,startY
        pt2 = endX,endY
        #copy out the boxes
        foo=img.copy()[startY:endY,startX:endX]
        #get the median
        threshvals[j-1] = np.median(foo)
    v=np.median(threshvals)
    #set the threshold to some level based on that value
    thresh=int(v*(1 - scan_settings.sigma))
    ret,img2 = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY_INV)
    #erode and dilate
    img2 = cv2.erode(img2,scan_settings.kern,iterations=3)
    img2 = cv2.dilate(img2,scan_settings.kern,iterations=3)
    return img2
    
def scanDots(img, areaDict, ignores, convDict):
    '''
    scans an aligned and thresholded image in the areas of areaDict
    returns a dictionry of results
    '''
    resDict = areaDict.fromkeys(areaDict,'-')
    #going through each search area, where k is the name and v are the search area coordinates    
    for k, v in sorted(areaDict.items()):
        if k[0]=='Q':
            if ignores:
                if int(k[1:]) in ignores:
                    # enter something to trigger ignore
                    resDict[k] = 'ignore'
                    continue
        #get the upper left and lower right of the search area box
        pt1 = v[0]
        pt2 = v[1]
        #isolate the image in the search area
        scanArea=img[pt1[1]:pt2[1],pt1[0]:pt2[0]]
        #find the countours in that area
        (_, cnts, _) = cv2.findContours(scanArea, 
                                        cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)
        #initiate a list for contour areas
        idx=[]
        for i in range(len(cnts)):
            if cv2.contourArea(cnts[i])<10: #eliminate contours with very small areas
                idx.append(i)
        if len(idx) > 0:
            cnts=np.delete(cnts, idx, 0)
        #if after the clean up no contours are found, enter a dash and go on
        if len(cnts)==0:
            resDict[k] = '-'
        #initiate a blank string for questions (required to allow multiple answers)
        elif k[0]=='Q':
            resDict[k] = ''
        #go through each found contour
        for c in cnts:
            #get bounding rectangle for the contour
            x,y,w,h = cv2.boundingRect(c)
            #for each contour, see if it enloses the center of each bubble
            #and return the value indicated by the dictionaries created above
            #if we're working with name bubbles
            if k[0]=='F':
                for lett, coord in convDict.items():
                    if x< coord < x+w:
                        resDict[k] = lett
            if k[0]=='N':
                for lett, coord in convDict.items():
                    if x < coord < x+w:
                        resDict[k] = lett
            #if we're working with ID numbers
            if k[0]=='I':
                for lett, coord in convDict.items():
                    if y < coord < y+h:
                        resDict[k] = lett
            #if we're working with questions
            if k[0]=='Q':
                for lett, coord in convDict.items():
                    if x < coord < x+w:
                        # test to see if the lett is already in the resDict
                        if lett not in resDict[k]:
                            resDict[k] = ''.join(sorted(resDict[k] + lett))
            if len(resDict[k]) == 0:
                resDict[k] = '-'    
    return resDict

def saveimg(image_list, i, scanimg):
    basename = image_list[i].split('.')[0] #includes full path, not extension
    pathname = basename.rsplit('/',1)[0]+'/' #just the path to the directory
    savename = pathname + 'aligned_' + '{0:03d}'.format(i) + '.jpg'
    cv2.imwrite(savename, scanimg)