# imports
import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well  
import matplotlib.pyplot as plt

class Camera:
    '''Camera sensor class including measurement matrix'''
    def __init__(self):
        self.f_i = 2095.5 # focal length i-coordinate
        self.f_j = 2095.5 # focal length j-coordinate
        self.c_i = 944.9 # principal point i-coordinate
        self.c_j = 640.2 # principal point j-coordinate 
        
    def get_hx(self, x):    
        # calculate nonlinear measurement expectation value h(x)   
        hx = np.zeros((2,1))
        # check and print error message if dividing by zero
        if x[0]==0:
            raise NameError('Jacobian not defined for x[0]=0!')
        else:
            hx[0,0] = self.c_i - self.f_i*x[1]/x[0] # project to image coordinates
            hx[1,0] = self.c_j - self.f_j*x[2]/x[0]
            return hx    
    
    def get_H(self, x):
        # calculate Jacobian H at current x from h(x)
        H = np.matrix(np.zeros((2, 6)))
        # check and print error message if dividing by zero
        if x[0]==0:
            raise NameError('Jacobian not defined for x[0]=0!')
        else:
            H[0,0] = self.f_i * x[1] / (x[0]**2)
            H[1,0] = self.f_j * x[2] / (x[0]**2)
            H[0,1] = -self.f_i / x[0]
            H[1,2] = -self.f_j / x[0]
            return H  
 
 
def calc_Jacobian(x):
    # calculate Jacobian for x
    cam = Camera()
    H = cam.get_H(x)

    # init visualization
    fig, (ax1, ax2) = plt.subplots(1,2)
    plot_x = []
    plot_y1 = []
    plot_y2 = []
    lin_y1 = []
    lin_y2 = []

    # calculate Taylor series expansion point
    hx_orig = cam.get_hx(x)
    ax1.plot(x[0], hx_orig[0], marker='x', color='green', label='expansion point x')
    ax2.plot(x[0], hx_orig[1], marker='x', color='green', label='expansion point x')

    # calculate linear approximation at this point 
    s1 = float(H[0,0]) # slope of tangent given by Jacobian H
    s2 = float(H[1,0])
    i1 = float(hx_orig[0] - s1*x[0]) # intercept i = y - s*x
    i2 = float(hx_orig[1] - s2*x[0])

    # calculate nonlinear measurement function h
    for px in range(1,50):
        x[0] = px
        hx = cam.get_hx(x)
        plot_x.append(px)
        plot_y1.append(hx[0])
        plot_y2.append(hx[1])
        lin_y1.append(s1*px + i1)
        lin_y2.append(s2*px + i2)
        
    # plot results
    ax1.plot(plot_x, plot_y1, color='blue', label='measurement function h')
    ax1.plot(plot_x, lin_y1, color='red', label='linear approximation H')
    ax2.plot(plot_x, plot_y2, color='blue', label='measurement function h')
    ax2.plot(plot_x, lin_y2, color='red', label='linear approximation H')

    # maximize window     
    mng = plt.get_current_fig_manager()
    mng.frame.Maximize(True)

    # legend
    ax1.legend(loc='center left', shadow=True, fontsize='large', bbox_to_anchor=(0.5, 0.1))
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('h(x) first component [px]')
    ax2.legend(loc='center left', shadow=True, fontsize='large', bbox_to_anchor=(0.5, 0.1))
    ax2.set_xlabel('x [m]')
    ax2.set_ylabel('h(x) second component [px]')

    plt.show()


#################
# define expansion point for Taylor series
x = np.matrix([[10],
            [1],
            [-1],
            [0],
            [0],
            [0]])

calc_Jacobian(x)

