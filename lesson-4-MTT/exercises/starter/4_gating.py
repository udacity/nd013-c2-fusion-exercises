# imports
import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well   
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats.distributions import chi2

class Association:
    '''Data association class with single nearest neighbor association and gating based on Mahalanobis distance'''
    def __init__(self):
        self.association_matrix = np.matrix([])
        self.unassigned_tracks = []
        self.unassigned_meas = []
        
    def associate(self, track_list, meas_list):
        N = len(track_list) # N tracks
        M = len(meas_list) # M measurements
        self.unassigned_tracks = list(range(N))
        self.unassigned_meas = list(range(M))
        
        # initialize association matrix
        self.association_matrix = np.inf*np.ones((N,M)) 
        
        # loop over all tracks and all measurements to set up association matrix
        for i in range(N): 
            track = track_list[i]
            for j in range(M):
                meas = meas_list[j]
                dist = self.MHD(track, meas)
                if self.gating(dist):
                    self.association_matrix[i,j] = dist
        
    def MHD(self, track, meas):
        # calc Mahalanobis distance
        H = np.matrix([[1, 0, 0, 0],
                       [0, 1, 0, 0]]) 
        gamma = meas.z - H*track.x
        S = H*track.P*H.transpose() + meas.R
        MHD = gamma.transpose()*np.linalg.inv(S)*gamma # Mahalanobis distance formula
        return MHD
    
    def gating(self, MHD): 
        # check if measurement lies inside gate

        ############
        # TODO: return True if measurement lies inside gate, otherwise return False
        ############
        
        return True
        
    def get_closest_track_and_meas(self):
        # find closest track and measurement for next update

        ############
        # TODO: 
        # - find indices of closest track and measurement for next update
        # - return NAN if no more associations can be found (i.e. minimum entry in association matrix is infinity)
        # - delete row and column in association matrix for closest track and measurement
        # - remove found track number from unassigned_tracks, meas number from unassigned_meas
        # - return indices of closest track and measurement for next update
        ############
        
        return np.nan, np.nan

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
    '''Measurement class with easurement, covariance, id'''
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
    print('unassigned_tracks list:', association.unassigned_tracks)
    print('unassigned_meas list:', association.unassigned_meas)     

    # visualize distances
    for track in track_list:
        for meas in meas_list:
            dist = association.association_matrix[track.id-1, meas.id-1]
            if dist < np.inf: 
                ax.plot([float(-track.x[1]), float(-meas.z[1])], [float(track.x[0]), float(meas.z[0])], color='gray')
                str_dist = "{:.2f}".format(dist)
                ax.text(float((-track.x[1] - meas.z[1])/2), float((track.x[0] + meas.z[0])/2), str_dist)

    # update associated tracks with measurements
    matrix_orig = association.association_matrix
    while association.association_matrix.shape[0]>0 and association.association_matrix.shape[1]>0:
        
        # search for next association between a track and a measurement
        ind_track, ind_meas = association.get_closest_track_and_meas()
        if np.isnan(ind_track):
            print('---no more associations---')
            break
            
        track = track_list[ind_track]
        meas = meas_list[ind_meas]
        dist = matrix_orig[ind_track, ind_meas]
        ax.plot([float(-track.x[1]), float(-meas.z[1])], [float(track.x[0]), float(meas.z[0])], color='blue', label='association')
        str_dist = "{:.2f}".format(dist)
        ax.text(float((-track.x[1] - meas.z[1])/2), float((track.x[0] + meas.z[0])/2), str_dist)
        print('found association between track', ind_track+1, 'and measurement', ind_meas+1, 'with MHD =', str_dist)
        print('New association matrix:', association.association_matrix)    
        print('New unassigned_tracks list:', association.unassigned_tracks)
        print('New unassigned_meas list:', association.unassigned_meas)        
        

    #################
    # visualization
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