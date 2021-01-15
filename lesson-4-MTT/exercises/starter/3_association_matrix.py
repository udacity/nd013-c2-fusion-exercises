# imports
import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well   
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Association:
    '''Data association class with single nearest neighbor association and gating based on Mahalanobis distance'''
    def __init__(self):
        self.association_matrix = np.matrix([])
        
    def associate(self, track_list, meas_list):
        N = len(track_list) # N tracks
        M = len(meas_list) # M measurements
        
        # initialize association matrix
        self.association_matrix = np.inf*np.ones((N,M)) 

        ############
        # TODO: fill association matrix with Mahalanobis distances between all tracks and all measurements
        ############
        
    def MHD(self, track, meas):
        # calc Mahalanobis distance

        ############
        # TODO: Calculate and return Mahalanobis distance between track and meas. 
        # You will also need to implement the measurement matrix H for 2D lidar measurements.
        # Note that the track is already given in sensor coordinates here, no transformation needed.
        ############
        
        return 0
    

################## 
class Track:
    '''Track class with state, covariance, id'''
    def __init__(self, id):
        # save id
        self.id = id
        
        # generate random state x
        self.x = np.matrix([[np.random.uniform(2,8)],
                        [np.random.uniform(-3,3)],
                        [0],
                        [0]])
        
        # set up estimation error covariance
        self.P = np.matrix([[2, 0, 0, 0],
                        [0, 3, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        
class Measurement:
    '''Measurement class with measurement, covariance, id'''
    def __init__(self, id, x, y):
        # save id
        self.id = id
        
        # generate random measurement z
        self.z = np.matrix([[x + np.random.normal(0,2)],
                        [y + np.random.normal(0,2)]])
        
        # set up measurement covariance
        self.R = np.matrix([[2, 0],
                        [0, 2]])
         
    
#################
def run():
    '''generate tracks and measurements and call association'''
    # set up track_list and meas_list for association
    np.random.seed(5) # make random values predictable
    association = Association() # init data association
    track_list = []
    meas_list = []

    # initialize visualization
    fig, ax = plt.subplots()

    # generate and plot tracks and measurements
    for i in range(3):
        
        # tracks
        track = Track(i+1)
        track_list.append(track)
        ax.scatter(float(-track.x[1]), float(track.x[0]), marker='x', color='red', label='track')
        ax.text(float(-track.x[1]), float(track.x[0]), str(track.id), color='red')
        
        # measurements
        meas = Measurement(i+1, float(track.x[0]), float(track.x[1]))
        meas_list.append(meas)
        ax.scatter(float(-meas.z[1]), float(meas.z[0]), marker='o', color='green', label='measurement')
        ax.text(float(-meas.z[1]), float(meas.z[0]), str(meas.id), color='green')

    # calculate association matrix
    association.associate(track_list, meas_list)
    print('Association matrix:', association.association_matrix)

    # visualize distances
    for track in track_list:
        for meas in meas_list:
            dist = association.association_matrix[track.id-1, meas.id-1]
            if dist < np.inf: 
                ax.plot([float(-track.x[1]), float(-meas.z[1])], [float(track.x[0]), float(meas.z[0])], color='gray')
                str_dist = "{:.2f}".format(dist)
                ax.text(float((-track.x[1] - meas.z[1])/2), float((track.x[0] + meas.z[0])/2), str_dist)

    # maximize window     
    mng = plt.get_current_fig_manager()
    mng.frame.Maximize(True)

    # remove repeated labels
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    ax.legend(handle_list, label_list, loc='center left', shadow=True, fontsize='large', bbox_to_anchor=(0.9, 0.1))

    # axis
    ax.set_xlabel('y [m]')
    ax.set_ylabel('x [m]')
    ax.set_xlim(-5,5)
    ax.set_ylim(0,10)

    # correct x ticks (positive to the left)
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(-x) if x!=0 else '{0:g}'.format(x))
    ax.xaxis.set_major_formatter(ticks_x)
            
    plt.show() 
    
####################
# call main loop
run()