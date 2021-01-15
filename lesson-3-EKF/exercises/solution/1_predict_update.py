import numpy as np

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.dim_state = 2 # process model dimension

    def F(self):
        # system matrix
        return np.matrix([[1, 1],
                        [0, 1]])

    def Q(self):
        # process noise covariance Q
        return np.matrix([[0, 0],
                        [0, 0]])
        
    def H(self):
        # measurement matrix H
        return np.matrix([[1, 0]])
    
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
    np.random.seed(10) # make random values predictable
    
    # init filter
    KF = Filter()
    
    # init track state and covariance
    x = np.matrix([[0],
                [0]])
    P = np.matrix([[5**2, 0],
                [0, 5**2]])  
    
    # loop over measurements and call predict and update
    for i in range(1,101):        
        print('------------------------------')
        print('processing measurement #' + str(i))
        
        # prediction
        x, P = KF.predict(x, P) # predict to next timestep
        print('x- =', x)
        print('P- =', P)
        
        # measurement generation
        sigma_z = 1 # measurement noise
        z = np.matrix([[i + np.random.normal(0, sigma_z)]]) # generate noisy measurement
        R = np.matrix([[sigma_z**2]]) # measurement covariance
        print('z =', z)
        
        # update
        x, P = KF.update(x, P, z, R) # update with measurement
        print('x+ =', x)
        print('P+ =', P)
        

# call main loop
run_filter()