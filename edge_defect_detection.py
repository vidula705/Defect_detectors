import cv2
import numpy as np
import sys

import __builtin__
#import Globals
import cv2.cv as cv
endif= """ pass """
endclass = """ pass """
enddef = """ pass """


class detect_edge_defect:
        def __init__(self):
                print "Edge_defect constructor init"
                self.statusflag = 0
                self.status = ""
        enddef

        def findDefect( self, img ):
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                #cv2.imshow("gray",gray)
                #cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)
                thresh = 30
                max_thresh = 255

                edges = cv2.Canny(gray,thresh,thresh*2)
                drawing = np.zeros(img.shape,np.uint8) # Image to draw the contours
                contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                #cv2.imshow("edges",edges)
                cv2.drawContours( gray, contours, -1, (0, 255, 0), 3 )
                
                for cnt in contours:
                        areas = [cv2.contourArea(cnt)]
                        max_index = np.argmax(areas)
                        cnt1=contours[max_index]
                        x,y,w,h = cv2.boundingRect(cnt1)
                        cv2.rectangle(edges,(x,y),(x+w,y+h),(255,255,255),2)
                        #cv2.imshow("Show",edges)

                hull = cv2.convexHull(cnt1,returnPoints = False)
                defects = cv2.convexityDefects(cnt1,hull)
    
                #print "h", h
                #print "w", w
                #print "x", x
                #print "y", y
                for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                #print "d", d
                depth= d/256 #distance between the farthest point and the convex hull
                #print "depth", depth            
                        
    
                hp = 40 # in cm
                wp = 20 # in cm
                phy_hight= hp * 10 #hp in mm
                phy_width= wp * 10 #wp in mm
                pixal_hight = float(h/phy_hight)
                if(pixal_hight == 0.00):
                        pixal_hight = 1
                pixal_width = float(w/phy_width)
                if(pixal_width == 0.00):
                        pixal_width= 1
                #print "pixal_hight", float(pixal_hight)
                #print "pixal_width", float(pixal_width)
                input_mm = 1 #in mm
                tolerance = input_mm * pixal_hight
                print "tolerance", tolerance
                if(depth == 0.00):
                        result = "No Edge Defect"
                        self.statusflag = 0
                        print result
                elif(tolerance < depth):
                        result = "No Edge Defect"
                        self.statusflag = 0
                        print result
                else:
                        result = "Edge Defect"
                        self.statusflag = 1
                        print result
                self.status = result

        enddef

        def storeResult(self):
               print "store colour defect result.."
        enddef
endclass

def loadInfo():
        theDetectors.Detectors.append(detect_edge_defect)
enddef

### Stand-Alone Application ###
"""
if __name__ == "__main__":
        print "Integrated module"
        detectInst = detect_edge_defect()       
        fname = "../../test/t6.jpg"
        image = cv2.imread(fname)
        if image is None:
                print 'Failed to load image file:', fname
                sys.exit(1)
        detectInst.findDefect(image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
"""
