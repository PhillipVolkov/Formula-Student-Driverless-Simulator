"""
This example shows how to retrieve lidar pointclouds.
Before running this you must add a lidar to your vehicle.
Add the following to your settings.json file in the Sensors section:

"ExampleLidar": {
    "SensorType": 6,
    "Enabled": true,
    "X": 1.3, "Y": 0, "Z": -0.3,
    "Roll": 0, "Pitch": 0, "Yaw" : 0,
    "NumberOfLasers": 15,
    "PointsPerScan": 4000,
    "VerticalFOVUpper": -5,
    "VerticalFOVLower": 5,
    "HorizontalFOVStart": -90,
    "HorizontalFOVEnd": 90,
    "RotationsPerSecond": 10,
    "DrawDebugPoints": true
}

"""

import sys
import os
import time
import numpy

## adds the fsds package located the parent directory to the pyhthon path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fsds

# connect to the AirSim simulator 
client = fsds.FSDSClient()

# Check network connection
client.confirmConnection()

lidardata = client.getLidarData(lidar_name = 'Lidar1')

# nanosecond timestamp of when the imu frame was captured
print("lidardata nano: ", lidardata.time_stamp)

# the location of the lidar at the moment of capture in global reference frame
print("lidar pose: ", lidardata.pose)

# Convert the list of floats into a list of xyz coordinates
points = numpy.array(lidardata.point_cloud, dtype=numpy.dtype('f4'))
points = numpy.reshape(points, (int(points.shape[0]/4), 4))

print("number of hit points: ", len(points))

print(f"Num Orange\t{numpy.count_nonzero(numpy.logical_and(points[:, 3] > 0.89, points[:, 3] < 0.91))}")
print(f"Num Blue\t{numpy.count_nonzero(numpy.logical_and(points[:, 3] > 0.79, points[:, 3] < 0.81))}")
print(f"Num Yellow\t{numpy.count_nonzero(numpy.logical_and(points[:, 3] > 0.69, points[:, 3] < 0.71))}")
print(f"Num Ground\t{numpy.count_nonzero(numpy.logical_and(points[:, 3] > 0.09, points[:, 3] < 0.11))}")
# for point in points:
#     x:float = point[0]
#     y:float = point[1]
#     z:float = point[2]
#     intesity = point[3]
#     # do something with these values    
#     if intesity > 0.15:
#         print("{:.3f}\t{:.3f}\t{:.3f}\t{:.20f}".format(x, y, z, intesity))