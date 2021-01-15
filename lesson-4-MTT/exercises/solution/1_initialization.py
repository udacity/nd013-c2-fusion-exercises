# imports
import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well  
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Track:
    '''Track class with state, covariance, id'''
    def __init__(self, meas, id):
        print('creating track no.', id)
        self.id = id
        
        # transform measurement to vehicle coordinates
        pos_sens = np.ones((4, 1)) # homogeneous coordinates
        pos_sens[0:3] = meas.z[0:3] 
        pos_veh = meas.sens_to_veh*pos_sens
        
        # save initial state from measurement
        self.x = np.zeros((6,1))
        self.x[0:3] = pos_veh[0:3]
        
        # set up position estimation error covariance
        M_rot = meas.sens_to_veh[0:3, 0:3]
        P_pos = M_rot * meas.R * np.transpose(M_rot)
        
        # set up velocity estimation error covariance
        sigma_p44 = 50 # initial setting for estimation error covariance P entry for vx
        sigma_p55 = 50 # initial setting for estimation error covariance P entry for vy
        sigma_p66 = 5 # initial setting for estimation error covariance P entry for vz
        P_vel = np.matrix([[sigma_p44**2, 0, 0],
                        [0, sigma_p55**2, 0],
                        [0, 0, sigma_p66**2]])
        
        # overall covariance initialization
        self.P = np.zeros((6, 6))
        self.P[0:3, 0:3] = P_pos
        self.P[3:6, 3:6] = P_vel
        
        
###################  
        
class Measurement:
    '''Lidar measurement class including measurement z, covariance R, coordinate transform matrix'''
    def __init__(self, gt, phi, t):
        # compute rotation around z axis
        M_rot = np.matrix([[np.cos(phi), -np.sin(phi), 0], 
                    [np.sin(phi), np.cos(phi), 0],
                    [0, 0, 1]])
        
        # coordiante transformation matrix from sensor to vehicle coordinates
        self.sens_to_veh = np.matrix(np.identity(4))            
        self.sens_to_veh[0:3, 0:3] = M_rot
        self.sens_to_veh[0:3, 3] = t
        print('Coordinate transformation matrix:', self.sens_to_veh)
        
        # transform ground truth from vehicle to sensor coordinates
        gt_veh = np.ones((4, 1)) # homogeneous coordinates
        gt_veh[0:3] = gt[0:3] 
        gt_sens = np.linalg.inv(self.sens_to_veh) * gt_veh
        
        # create measurement object
        sigma_lidar_x = 0.01 # standard deviation for noisy measurement generation
        sigma_lidar_y = 0.01
        sigma_lidar_z = 0.001
        self.z = np.zeros((3,1)) # measurement vector
        self.z[0] = float(gt_sens[0,0]) + np.random.normal(0, sigma_lidar_x)
        self.z[1] = float(gt_sens[1,0]) + np.random.normal(0, sigma_lidar_y)
        self.z[2] = float(gt_sens[2,0]) + np.random.normal(0, sigma_lidar_z)
        self.R = np.matrix([[sigma_lidar_x**2, 0, 0], # measurement noise covariance matrix
                            [0, sigma_lidar_y**2, 0], 
                            [0, 0, sigma_lidar_z**2]])
        
def visualize(track, meas):
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    ax1.scatter(-meas.z[1], meas.z[0], marker='o', color='blue', label='measurement')
    ax2.scatter(-track.x[1], track.x[0], color='red', s=80, marker='x', label='initialized track')

    # transform measurement to vehicle coordinates for visualization
    z_sens = np.ones((4, 1)) # homogeneous coordinates
    z_sens[0:3] = meas.z[0:3] 
    z_veh = meas.sens_to_veh * z_sens
    ax3.scatter(-float(z_veh[1]), float(z_veh[0]), marker='o', color='blue', label='measurement')
    ax3.scatter(-track.x[1], track.x[0], color='red', s=80, marker='x', label='initialized track')
        
    # maximize window     
    mng = plt.get_current_fig_manager()
    mng.frame.Maximize(True)

    # legend and axes
    for ax in (ax1, ax2, ax3):
        ax.legend(loc='center left', shadow=True, fontsize='large', bbox_to_anchor=(0.5, 0.1))
        ax.set_xlabel('y [m]')
        ax.set_ylabel('x [m]')
        ax.set_xlim(-2,2)
        ax.set_ylim(0,2)
        # correct x ticks (positive to the left)
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(-x) if x!=0 else '{0:g}'.format(x))
        ax.xaxis.set_major_formatter(ticks_x)
        
    # titles
    ax1.title.set_text('Sensor Coordinates')
    ax2.title.set_text('Vehicle Coordinates')
    ax3.title.set_text('Vehicle Coordinates\n (track and measurement should align)')

    plt.show()

        
###################  
# ground truth         
gt = np.matrix([[1.7],
                [1],
                [0]])

# sensor translation and rotation angle
t = np.matrix([[2],
                [0.5],
                [0]])
phi = np.radians(45)

# generate measurement
meas = Measurement(gt, phi, t)

# initialize track from this measurement
track = Track(meas, 1)

# visualization
visualize(track, meas)