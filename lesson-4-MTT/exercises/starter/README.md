# Exercises Multi-Target Tracking

Here are the instructions for the MTT exercises.

## 1_initialization.py

In this exercise, you will implement a track initialization based on an unassigned measurement. 

### Your Task

In the `__init__()` function of the Track class, please initialize the 6x1 numpy matrix `x` and the 6x6 numpy matrix `P` based on the measurement input `meas`. The measurement input is an instance of the `Measurement` class. The `Measurement` class already contains the correct transformation matrix including rotation and translation from sensor to vehicle coordinates.

### Desired Result

If you run the script, the left plot contains the test measurement in sensor coordinates. We want to use this measurement to initialize a new track. The second plot shows the initialized track. Finally, the last plot shows the measurement converted to vehicle coordinates and the initialized track. If you have implemented everything correctly, the track should be initialized where the measurement lies, so the blue and red marker should align.

## 2_fov.py

In this exercise, you will implement a sensor visibility check.

### Your Task

In the `Camera` class, please implement the function `in_fov()`. It takes the current state x as an input and should return true if x lies in the camera's field of view, otherwise it should return false. The `Camera` class contains a given field of view `fov` that you should use. Don't forget to transform from vehicle to sensor coordinates with the given transformation matrices.

### Desired Result

If you run the script, you can see the opening angle of the camera in blue, so the visible range is in the area between the blue lines. The script generates random points and calculates whether the points lie inside the field of view. If you have implemented everything correctly, the result should be `False` for all red points outside the field of view, but the visible points in between the blue lines should be green and return `True`. 


## 3_association_matrix.py

In this exercise, you will implement the association matrix for a simple association problem with 3 tracks and 3 measurements. 

### Your Task

In the `Association` class, please implement the attribute `association_matrix` in the function called `associate()`. This function gets as input a list of N track indices `track_list` and a list of M measurement indices `meas_list`. The association matrix is initialized to an NxM matrix with matrix components set to infinity. Now please fill the association matrix with the respective Mahalanobis distances. To calculate these distances, please implement the `MHD()` function below that gets a track `track` and a measurement `meas` as input and returns the Mahalanobis distance. You will also have to implement the measurement function H here for a 4D state vector and a 2D lidar measurement. We neglect the height in this exercise, as well as the transformation from vehicle to sensor coordinates, so the track state is already given in sensor coordinates here.


### Desired Result

If you run the script, the figure contains 3 tracks in red and 3 measurements in green. If you have implemented everything correctly, the script links all associated track-measurement-pairs with gray lines and writes the calculated MHD next to it. The console output shows how the resulting association matrix looks like.

## 4_gating.py

In this exercise, you will implement a gating function and a track-measurement-association.

### Your Task

 First, please implement the `gating()` function based on the inverse cumulative chi-square-distribution. The function should return `True` if the measurement lies inside the gate, otherwise `False`. You can use a gating threshold of 0.95, for example.

Second, please implement the function called `get-closest-track-and-meas()`, which should return the closest track and measurement for the next update. You have to search the association matrix for the smallest entry. If the association matrix only contains infinity as entries, please return `numpy.nan`. Otherwise, you should delete the row and column of the minimum entry from the matrix and get the right track number and measurement number from the lists `unassigned_tracks` and `unassigned_measurements`, respectively. Finally, please delete the corresponding entries from the lists `unassigned_tracks` and `unassigned_measurements` and return the track and the measurement. 

### Desired Result

If you run the script initially, all track-measurement-combinations are plotted with gray lines. After completion, there should be less gray lines, unlikely associations should have been removed. Also, blue lines should show which track got associated to which measurement.

You can also see in the console output how the initial 3x3 association matrix is decreases step by step until it is empty.