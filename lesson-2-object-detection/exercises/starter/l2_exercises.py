# ---------------------------------------------------------------------
# Exercises from lesson 2 (object detection)
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.  
#
# Purpose of this file : Starter Code
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

from PIL import Image
import io
import sys
import os
import cv2
import open3d as o3d
import math
import numpy as np
import zlib

import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well     
import matplotlib.pyplot as plt

# Exercise C2-4-6 : Plotting the precision-recall curve
def plot_precision_recall(): 

    # Please note: this function assumes that you have pre-computed the precions/recall value pairs from the test sequence
    #              by subsequently setting the variable configs.conf_thresh to the values 0.1 ... 0.9 and noted down the results.
    
    # Please create a 2d scatter plot of all precision/recall pairs 



# Exercise C2-3-4 : Compute precision and recall
def compute_precision_recall(det_performance_all, conf_thresh=0.5):

    if len(det_performance_all)==0 :
        print("no detections for conf_thresh = " + str(conf_thresh))
        return
    
    # extract the total number of positives, true positives, false negatives and false positives
    # format of det_performance_all is [ious, center_devs, pos_negs]

    #print("TP = " + str(true_positives) + ", FP = " + str(false_positives) + ", FN = " + str(false_negatives))
    
    # compute precision
    
    # compute recall 

    #print("precision = " + str(precision) + ", recall = " + str(recall) + ", conf_thres = " + str(conf_thresh) + "\n")    
    



# Exercise C2-3-2 : Transform metric point coordinates to BEV space
def pcl_to_bev(lidar_pcl, configs, vis=True):

    # compute bev-map discretization by dividing x-range by the bev-image height

    # create a copy of the lidar pcl and transform all metrix x-coordinates into bev-image coordinates    

    # transform all metrix y-coordinates as well but center the foward-facing x-axis on the middle of the image

    # shift level of ground plane to avoid flipping from 0 to 255 for neighboring pixels

    # re-arrange elements in lidar_pcl_cpy by sorting first by x, then y, then by decreasing height

    # extract all points with identical x and y such that only the top-most z-coordinate is kept (use numpy.unique)

    # assign the height value of each unique entry in lidar_top_pcl to the height map and 
    # make sure that each entry is normalized on the difference between the upper and lower height defined in the config file
    
    # sort points such that in case of identical BEV grid coordinates, the points in each grid cell are arranged based on their intensity

    # only keep one point per grid cell

    # create the intensity map

    # visualize intensity map
    #if vis:
    #    img_intensity = intensity_map * 256
    #    img_intensity = img_intensity.astype(np.uint8)
    #    while (1):
    #        cv2.imshow('img_intensity', img_intensity)
    #        if cv2.waitKey(10) & 0xFF == 27:
    #            break
    #    cv2.destroyAllWindows()

