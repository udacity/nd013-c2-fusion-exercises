# ---------------------------------------------------------------------
# "Loop over Waymo frames : Starting place for lesson exercises"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Loop over all frames in a Waymo Open Dataset file
#                        and perform basic operations on the data
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

##################
# Imports

# general package imports
import os
import sys
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import copy
import zlib
from easydict import EasyDict as edict

# Add current working directory to path
sys.path.append(os.getcwd())

# Waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import WaymoDataFileReader, dataset_pb2, label_pb2
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils

# misc. project-related imports
import misc.objdet_tools as tools
from misc.helpers import load_object_from_file

# add exercise directories to python path to enable relative imports
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
EXE_L1 = 'lesson-1-lidar-sensor/exercises/starter'
EXA_L1 = 'lesson-1-lidar-sensor/examples'
EXE_L2 = 'lesson-2-object-detection/exercises/starter'
EXA_L2 = 'lesson-2-object-detection/examples'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, EXE_L1)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, EXA_L1)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, EXE_L2)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, EXA_L2)))

# import functions from individual exercise files
import l2_examples
import l2_exercises
import l1_examples
import l1_exercises


##################
# Set parameters and perform initializations

# Select Waymo Open Dataset file and frame numbers
data_filename = 'training_segment-1005081002024129653_5313_150_5333_150_with_camera_labels.tfrecord' # Sequence 1
#data_filename = 'training_segment-10072231702153043603_5725_000_5745_000_with_camera_labels.tfrecord' # Sequence 2
# data_filename = 'training_segment-10963653239323173269_1924_000_1944_000_with_camera_labels.tfrecord'  # Sequence 3
show_only_frames = [0, 10]  # show only frames in interval for debugging

# set pause time between frames in ms (0 = stop between frames until key is pressed)
vis_pause_time = 0  

# Prepare Waymo Open Dataset file for loading
data_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset', data_filename)  # adjustable path in case this script is called from another working directory
results_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results')
datafile = WaymoDataFileReader(data_fullpath)
datafile_iter = iter(datafile)  # initialize dataset iterator

##################
# Perform detection & tracking over all selected frames

cnt_frame = 0
det_performance_all = []  # used for exercises in C2-4
while True:
    try:
        #################################
        # Get next frame from Waymo dataset

        frame = next(datafile_iter)
        if cnt_frame < show_only_frames[0]:
            cnt_frame = cnt_frame + 1
            continue
        elif cnt_frame > show_only_frames[1]:
            print('reached end of selected frames')
            break

        print('------------------------------')
        print('processing frame #' + str(cnt_frame))

        # Usage instruction : When working on a specific exercise, 
        # simply uncomment the respective function calls and open 
        # the implementation for more details

        ####### LESSON 1 EXERCISES & EXAMPLES START #######
        #######

        lidar_name = dataset_pb2.LaserName.TOP

        # Exercise C1-3-1 : print no. of vehicles
        # l1_exercises.print_no_of_vehicles(frame) 

        # Example C1-3-2 : display camera image
        # l1_examples.display_image(frame)

        # Example C1-3-3 : print angle of vertical field of view
        # l1_examples.print_vfov_lidar(frame, lidar_name)

        # Example C1-5-1 : Load range image
        # l1_examples.print_range_image_shape(frame, lidar_name)

        # Exercise C1-5-2 : Compute pitch angle resolution
        # l1_exercises.print_pitch_resolution(frame, lidar_name)

        # Example C1-5-3 : Retrieve maximum and minimum distance
        # l1_examples.get_max_min_range(frame, lidar_name)

        # Example C1-5-4 : Visualize range channel
        # l1_examples.vis_range_channel(frame, lidar_name)

        # Exercise C1-5-5 : Visualize intensity channel
        # l1_exercises.vis_intensity_channel(frame, lidar_name)

        # Example C1-5-6 : Convert range image to 3D point-cloud
        # l1_examples.range_image_to_point_cloud(frame, lidar_name)

        #######
        ####### LESSON 1 EXERCISES & EXAMPLES  END #######


        ####### LESSON 2 EXERCISES & EXAMPLES  START #######
        #######

        # Define parameters used in subsequent steps
        configs = edict()
        configs.lim_x = [0, 50]
        configs.lim_y = [-25, 25]
        configs.lim_z = [-0.3, 3]
        configs.bev_width = 608
        configs.bev_height = 608
        configs.conf_thresh = 0.5
        configs.model = 'darknet'

        # Example C2-3-1 : Crop point cloud
        # lidar_pcl = l1_examples.range_image_to_point_cloud(frame, lidar_name, True)
        # cropped_pcl = l2_examples.crop_pcl(lidar_pcl, configs, False)

        # Exercise C2-3-2 : Transform metric point coordinates to BEV space
        # l2_exercises.pcl_to_bev(cropped_pcl, configs)

        # Example C2-3-3 : Minimum and maximum intensity
        # l2_examples.min_max_intensity(lidar_pcl)

        # Example C2-4-2 : count total no. of vehicles and vehicles that are difficult to track
        # l2_examples.count_vehicles(frame)

        # Example C2-4-3 : Display label bounding boxes on top of BEV map
        #lidar_bev = load_object_from_file(results_fullpath, data_filename, 'lidar_bev', cnt_frame)
        #lidar_bev_labels = l2_examples.render_bb_over_bev(lidar_bev, frame.laser_labels, configs)

        # Example C2-4-4 : Display detected objects on top of BEV map
        #detections = load_object_from_file(results_fullpath, data_filename, 'detections_' + configs.model + '_' + str(configs.conf_thresh), cnt_frame)
        #l2_examples.render_obj_over_bev(detections, lidar_bev_labels, configs, True)

        # Exercise C2-4-5 : Compute precision and recall (part 1/2 - remove comments only, no action inside functions required)
        #det_performance = load_object_from_file(results_fullpath, data_filename, 'det_performance_' + configs.model + '_' + str(configs.conf_thresh), cnt_frame)
        #det_performance_all.append(det_performance)  # store all evaluation results in a list for performance assessme

        #######
        ####### LESSON 2 EXERCISES & EXAMPLES  END #######

        # increment frame counter
        cnt_frame = cnt_frame + 1

    except StopIteration:
        # if StopIteration is raised, break from loop
        break

    # Exercise C2-4-5 : Compute precision and recall (part 2/2)
    # l2_exercises.compute_precision_recall(det_performance_all)

    # Exercise C2-4-6 : Plotting the precision-recall curve
    # l2_exercises.plot_precision_recall()
