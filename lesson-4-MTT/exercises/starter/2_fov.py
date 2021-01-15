# imports
import numpy as np
import matplotlib
matplotlib.use('wxagg') # change backend so that figure maximizing works on Mac as well   
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Camera:
    '''Camera sensor class including field of view and coordinate transformation'''
    def __init__(self, phi, t):
        self.fov = [-np.pi/4, np.pi/4] # sensor field of view / opening angle
        
        # compute rotation around z axis
        M_rot = np.matrix([[np.cos(phi), -np.sin(phi), 0],
                    [np.sin(phi), np.cos(phi), 0],
                    [0, 0, 1]])
        
        # coordiante transformation matrix from sensor to vehicle coordinates
        self.sens_to_veh = np.matrix(np.identity(4))            
        self.sens_to_veh[0:3, 0:3] = M_rot
        self.sens_to_veh[0:3, 3] = t
        self.veh_to_sens = np.linalg.inv(self.sens_to_veh) # transformation vehicle to sensor coordinates
    
    def in_fov(self, x):
        # check if an object x can be seen by this sensor

        ############
        # TODO: Return True if x lies in sensor's field of view, otherwise return False. 
        # Don't forget to transform from vehicle to sensor coordinates.
        ############
            
        return False
        
#################
def run():
    '''generate random points and check visibility'''
    # camera with translation and rotation angle
    t = np.matrix([[2],
                    [0],
                    [0]])
    phi = np.radians(45)
    cam = Camera(phi, t)

    # initialize visualization
    fig, ax = plt.subplots()

    for i in range(50):
        # define track position and velocity
        x = np.matrix([[np.random.uniform(-5,5)],
                    [np.random.uniform(-5,5)],
                    [0],
                    [0],
                    [0],
                    [0]])

        # check if x is visible by camera
        result = cam.in_fov(x)
        
        # plot results
        pos_veh = np.ones((4, 1)) # homogeneous coordinates
        pos_veh[0:3] = x[0:3] 
        pos_sens = cam.veh_to_sens*pos_veh # transform from vehicle to sensor coordinates
        if result == True:
            col = 'green'
            ax.scatter(float(-pos_sens[1]), float(pos_sens[0]), marker='o', color=col, label='visible track')
        else:
            col = 'red'
            ax.scatter(float(-pos_sens[1]), float(pos_sens[0]), marker='o', color=col, label='invisible track')
        ax.text(float(-pos_sens[1]), float(pos_sens[0]), str(result))
        
    # plot FOV    
    ax.plot([0, -5], [0, 5], color='blue', label='field of view') 
    ax.plot([0, 5], [0, 5], color='blue')

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
    ax.set_ylim(0,5)

    # correct x ticks (positive to the left)
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(-x) if x!=0 else '{0:g}'.format(x))
    ax.xaxis.set_major_formatter(ticks_x)

    plt.show() 

####################
# call main loop
run()