# ---------------------------------------------------------------------
# Exercises from lesson 2 (object detection)
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.  
#
# Purpose of this file : Examples
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

## Add current working directory to path
sys.path.append(os.getcwd())

## Waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2
import misc.objdet_tools as tools


# Example C2-4-3 : Display detected objects on top of BEV map
def render_obj_over_bev(detections, lidar_bev_labels, configs, vis=False):

    # project detected objects into bird's eye view
    tools.project_detections_into_bev(lidar_bev_labels, detections, configs, [0,0,255])

    # display bev map
    if vis==True:
        lidar_bev_labels = cv2.rotate(lidar_bev_labels, cv2.ROTATE_180)   
        cv2.imshow("BEV map", lidar_bev_labels)
        cv2.waitKey(0) 



# Example C2-4-3 : Display label bounding boxes on top of bev map
def render_bb_over_bev(bev_map, labels, configs, vis=False):

    # convert BEV map from tensor to numpy array
    bev_map_cpy = (bev_map.squeeze().permute(1, 2, 0).numpy() * 255).astype(np.uint8)
    bev_map_cpy = cv2.resize(bev_map_cpy, (configs.bev_width, configs.bev_height))

    # convert bounding box format format and project into bev
    label_objects = tools.convert_labels_into_objects(labels, configs)
    tools.project_detections_into_bev(bev_map_cpy, label_objects, configs, [0,255,0])
    
    # display bev map
    if vis==True:
        bev_map_cpy = cv2.rotate(bev_map_cpy, cv2.ROTATE_180)   
        cv2.imshow("BEV map", bev_map_cpy)
        cv2.waitKey(0)          

    return bev_map_cpy 

    

# Example C2-4-2 : count total no. of vehicles and vehicles that are difficult to track
def count_vehicles(frame):

    # initialze static counter variables
    if not hasattr(count_vehicles, "cnt_vehicles"):
        count_vehicles.cnt_vehicles = 0
        count_vehicles.cnt_difficult_vehicles = 0

    # loop over all labels
    for label in frame.laser_labels:

        if label.type == label_pb2.Label.Type.TYPE_VEHICLE:
            count_vehicles.cnt_vehicles += 1
            if label.detection_difficulty_level > 0:
                count_vehicles.cnt_difficult_vehicles += 1

    print("no. of labelled vehicles = " + str(count_vehicles.cnt_vehicles) + ", no. of vehicles difficult to detect = " + str(count_vehicles.cnt_difficult_vehicles))


# Example C2-3-3 : Minimum and maximum intensity
def min_max_intensity(lidar_pcl):

    # retrieve min. and max. intensity value from point cloud
    min_int = np.amin(lidar_pcl[:,3])
    max_int = np.amax(lidar_pcl[:,3])

    print("min. intensity = " + str(min_int) + ", max. intensity = " + str(max_int))


# Example C2-3-1 : Crop point cloud
def crop_pcl(lidar_pcl, configs, vis=True):

    # remove points outside of detection cube defined in 'configs.lim_*'
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]

    # visualize point-cloud
    if vis:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(lidar_pcl)
        o3d.visualization.draw_geometries([pcd])

    return lidar_pcl
