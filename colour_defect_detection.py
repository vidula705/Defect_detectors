# -*- coding: utf-8 -*-
import __builtin__
#import Globals
import cv2.cv as cv
import cv2
import sys
import numpy
from PIL import Image
from numpy import *
endif= """ pass """
endclass = """ pass """
enddef = """ pass """


class detect_colour_defect:
        H = 0
        W = 0
        h = 0
        w = 0

        def __init__(self):
                print "colour_defect constructor init"
                self.statusflag = 0
                self.status = ""
        enddef

        def findDefect( self, image ):

                img_list = ["img1", "img2","img3","img4", "img5", "img6", "img7", "img8", "img9"];
                imarray  = ["a1","a2","a3","a4","a5","a6","a7","a8","a9"];
                B_hist =["h1", "h2", "h3", "h4", "h5", "h6","h7","h8","h9"]
                G_hist =["h1", "h2", "h3", "h4", "h5", "h6","h7","h8","h9"]
                R_hist =["h1", "h2", "h3", "h4", "h5", "h6","h7","h8","h9"]
                B_corln =["c1", "c2", "c3", "c4", "c5", "c6","c7","c8","c9","c10","c11","c12", "c13", "c14", "c15", "c16","c17","c18","c19","c20","c21", "c22", "c23", "c24", "c25", "c26","c27","c28","c29","c30","c31", "c32", "c33", "c34", "c35", "c36","c37","c38","c39","c40"]
                G_corln =["c1", "c2", "c3", "c4", "c5", "c6","c7","c8","c9","c10","c11","c12", "c13", "c14", "c15", "c16","c17","c18","c19","c20","c21", "c22", "c23", "c24", "c25", "c26","c27","c28","c29","c30","c31", "c32", "c33", "c34", "c35", "c36","c37","c38","c39","c40"]
                R_corln= ["c1", "c2", "c3", "c4", "c5", "c6","c7","c8","c9","c10","c11","c12", "c13", "c14", "c15", "c16","c17","c18","c19","c20","c21", "c22", "c23", "c24", "c25", "c26","c27","c28","c29","c30","c31", "c32", "c33", "c34", "c35", "c36","c37","c38","c39","c40"]

                cnt =0
                B_Mean =0
                G_Mean =0
                R_Mean =0

                img_mat = cv.fromarray(image[:,:])
 
                # get cropping size 
                H,W = self.get_dim(image)
                h =H/3
                w= W/3

                # print h, w
                # Initialise arrays and variables 
 
                # Crop image in 9 equal parts """
                for ii in range(3):
                    w1 = w* ii
                    for jj in range(3):
                           h1 = h* jj
                           img = cv.GetSubRect( img_mat,(w1,h1,w,h) )
                           imarray[cnt] =numpy.asarray(img)
                           B_hist[cnt],G_hist[cnt],R_hist[cnt] = self.cal_hist(imarray[cnt])
                           cnt = cnt +1
   
                #calculate correlation of   9 parts of image with reference to each other
                #(histograme elements B,G,R respctivaly.c1 =h1,h2, c2 = h1, h3.. c8 = h1,h9; c9 = h2,h3,...c16=h2,h9, ......c72 = h8,h9) 
                cnt = 0
                ii =  0 
                jj =  0 
                for ii in range(9):
                  n = ii+1
                  #print "jj=", jj
                  for jj in range(n,9):
                      # print "cnt =", cnt , "ii =", ii, "jj =", jj
                      B_corln[cnt]= cv2.compareHist( B_hist[ii],  B_hist[jj], 0)
                      G_corln[cnt]= cv2.compareHist( G_hist[ii],  G_hist[jj], 0)
                      R_corln[cnt]= cv2.compareHist( R_hist[ii],  R_hist[jj], 0)
                      cnt = cnt +1

                #total corelation element per histogram B,G, R          
                N = cnt;      
 
                #calculate mean
                #TEST List:    
                #for val in B_corln:        # Second Example
                #   print 'Current val :', val
   
                for val in  range(N):
                    #print B_corln[val]
                    B_Mean = B_Mean + B_corln[val]
                    R_Mean = R_Mean + R_corln[val]
                    G_Mean = G_Mean + G_corln[val]

                # print "total val", B_Mean
                B_Mean = B_Mean/N
                G_Mean = G_Mean/N
                R_Mean = R_Mean/N

   
                # calculate standard deviation
                B_summation =0
                G_summation =0
                R_summation =0
                    
                for val in range(N):
                   diff =  B_corln[val] - B_Mean
                   diff = diff *diff
                   B_summation = B_summation + diff
                   diff =  G_corln[val] - G_Mean
                   diff = diff *diff
                   G_summation = G_summation + diff
                   diff =  R_corln[val] - R_Mean
                   diff = diff *diff
                   R_summation = R_summation + diff
                B_variance = B_summation/N
                B_St_dev = sqrt(B_variance);
                G_variance = G_summation/N
                G_St_dev = sqrt(G_variance);
                R_variance = R_summation/N
                R_St_dev = sqrt(R_variance);
    
                #print "B_Mean = ", B_Mean,"B_St_dev", B_St_dev
               # print "G_Mean = " ,G_Mean,"G_St_dev", G_St_dev
               # print "R_Mean = " ,R_Mean,"R_St_dev", R_St_dev

                # gray scale mean
                # Y´ = 0.299 * R´ + 0.587 * G´ + 0.114 * B´

                Mean =  (0.299 * R_Mean) + (0.587 * G_Mean) + (0.114 * B_Mean)
                print "final Mean =", Mean

                st_dev =   (B_St_dev + G_St_dev + R_St_dev)/3
                print " avrage st deviation =", st_dev
    
                if ( Mean < 0.4):
                   result = "Colour Defect"                   
                   self.statusflag = 1
                   #print result
                elif (0.4 < Mean <= 0.6 ):
                   if (st_dev <=0.35):
                        result = "No Colour Defect"
                        self.statusflag = 0
                        #print result
                   else:
                        result = "Colour Defect"
                        self.statusflag = 1
                        #print result
                else :      
                    result= "No Colour Defect"
                    self.statusflag = 0
                    #print result
                self.status = result
                #print  H,"\t", W, "\t",h,"\t", w,"\t", "%.3f" %B_Mean,"\t","%.3f" %G_Mean,"\t", "%.3f" %R_Mean, "\t", "%.3f" %Mean,"\t", "%.3f" %st_dev #,"\t",result
                #print result
        enddef

        def get_dim(self, img):
           #"""convert img to gray to get the height and width of the source image
           #""" TODO: w., h extracion from RGB image """
            grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
            h, w = grayImg.shape[:2]
           # print h,w
            return h,w
        enddef

        def cal_hist(self,inp_img):
           B_hist = cv2.calcHist(inp_img,[0],None,[256],[0,256])
           G_hist = cv2.calcHist(inp_img,[1],None,[256],[0,256])
           R_hist = cv2.calcHist(inp_img,[2],None,[256],[0,256])
           return B_hist   ,  G_hist,  R_hist
        enddef
       
        def storeResult(self):
               print "store colour defect result.."
        enddef
endclass


### For integration to CTIF ###
def loadInfo():
        theDetectors.Detectors.append(detect_colour_defect)
enddef

### Stand Alone Application ###
"""
if __name__ == "__main__":
    print "Integrated module"        
    detectInst = detect_colour_defect()    
    for index in range(1, 21):
        fname = "red_ceramic_tiles.jpg"
        img = cv2.imread(fname)
        imarray =numpy.asarray(img[:,:])
        if img is None:
            print 'Failed to load image file:', fname
            sys.exit(1)
        detectInst.findDefect( img )

    endif
"""
