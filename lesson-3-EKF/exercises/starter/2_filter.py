import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well  
import matplotlib.pyplot as plt

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.dim_state = 4 # process model dimension
        self.dt = 0.1 # time increment
        self.q=0.1 # process noise variable for Kalman filter Q

    def F(self):
        # system matrix

        ############
        # TODO: implement and return F
        ############
        
        pass

    def Q(self):
        # process noise covariance Q

        ############
        # TODO: implement and return Q
        ############
        
        pass
    
    def H(self):
        # measurement matrix H

        ############
        # TODO: implement and return H
        ############
    
        pass
    
    def predict(self, x, P):
        # predict state and estimation error covariance to next timestep
        F = self.F()
        x = F*x # state prediction
        P = F*P*F.transpose() + self.Q() # covariance prediction
        return x, P

    def update(self, x, P, z, R):
        # update state and covariance with associated measurement
        H = self.H() # measurement matrix
        gamma = z - H*x # residual
        S = H*P*H.transpose() + R # covariance of residual
        K = P*H.transpose()*np.linalg.inv(S) # Kalman gain
        x = x + K*gamma # state update
        I = np.identity(self.dim_state)
        P = (I - K*H) * P # covariance update
        return x, P   
        
        
def run_filter():
    ''' loop over data and call predict and update'''
    np.random.seed(0) # make random values predictable
    
    # init filter
    KF = Filter()
    
    # init figure
    fig, ax = plt.subplots()
    
    # init track state and covariance
    x = np.matrix([[0],
                [0],
                [0],
                [0]])
    P = np.matrix([[0.1**2, 0, 0, 0],
                [0, 0.1**2, 0, 0],
                [0, 0, 2**2, 0],
                [0, 0, 0, 2**2]])
    
    # loop over measurements and call predict and update
    for i in range(1,101):        
        
        # prediction
        x, P = KF.predict(x, P) # predict to next timestep
        
        # ground truth generation
        gt = np.matrix([[i*KF.dt], 
                       [0.1*(i*KF.dt)**2]])
        
        # measurement generation
        sigma_z = 0.2 # measurement noise 
        z = np.matrix([[float(gt[0]) + np.random.normal(0, sigma_z)],
                       [float(gt[1]) + np.random.normal(0, sigma_z)]]) # generate noisy measurement
        R = np.matrix([[sigma_z**2, 0], # measurement noise covariance matrix
                            [0, sigma_z**2]])
        
        # update
        x, P = KF.update(x, P, z, R) # update with measurement
        
        # visualization    
        ax.scatter(float(x[0]), float(x[1]), color='green', s=40, marker='x', label='track')
        ax.scatter(float(z[0]), float(z[1]), color='blue', marker='.', label='measurement')
        ax.scatter(float(gt[0]), float(gt[1]), color='gray', s=40, marker='+', label='ground truth')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_xlim(0,10)
        ax.set_ylim(0,10)
           
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
        ax.legend(handle_list, label_list, loc='center left', shadow=True, fontsize='x-large', bbox_to_anchor=(0.8, 0.5))

        plt.pause(0.01)
    plt.show()
        

####################
# call main loop
run_filter()