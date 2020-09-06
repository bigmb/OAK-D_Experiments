"""
Description : 
=============

This code is a simple example of how to get started with the depthai API. It shows how to :
1. Initialise the device.
2. Read and display the disparity map from the device in gray scale format.

This code can be helpful to get started with experiments involving depth information.
The beauty of OAK-D is that it makes the process of generating the disparity map information super easy.

Useage:
    python3 code4.py
"""

import sys
sys.path.append('/home/pi/depthai/')
import consts.resource_paths
import cv2
import depthai
import numpy as np

device = depthai.Device()

if not device:
    raise RuntimeError("Error initializing device. Try to reset it.")

pipeline = device.create_pipeline(config={
    'streams': ['left', 'right', 'metaout',{'name': 'disparity', 'max_fps': 30.0}],
    'ai': {
        "blob_file": consts.resource_paths.blob_fpath,
        "blob_file_config": consts.resource_paths.blob_config_fpath,
    },
    'camera': {'mono': {'resolution_h': 400, 'fps': 30}},
    'depth':
      {
          'calibration_file': consts.resource_paths.calib_fpath,
          'padding_factor': 0.3,
          'depth_limit_m': 10.0, # In meters, for filtering purpose during x,y,z calc
          'confidence_threshold' : 0.5, #Depth is calculated for bounding boxes with confidence higher than this number 
      }
})

if pipeline is None:
    raise RuntimeError('Pipeline creation failed!')

left_frame = None
right_frame = None
cv2.namedWindow("Left and Right Frames",0)
cv2.resizeWindow("Left and Right Frames",800,400)

while True:
    nnet_packets, data_packets = pipeline.get_available_nnet_and_data_packets()
    frame_present = False
    for packet in data_packets:
        if packet.stream_name == 'right':
            right_frame = packet.getData()
            frame_present = True
        elif packet.stream_name == 'disparity':
            disp = packet.getData()
            disp = (disp - np.min(disp))*1.0/(np.max(disp)-np.min(disp))
            cv2.imshow("disparity map",disp)
            frame_present = True
        else :
            frame_present = False

        if frame_present:
            try:
                output = np.hstack((right_frame/255.0,disp))
                cv2.imshow("modified image",output)
            except:
                print("Disparity and image could not be merged")

        
    
    if frame_present:
        try:
            out = np.hstack((left_frame,right_frame))
            cv2.imshow("Left and Right Frames",out)
            print("Left frame shape",left_frame.shape)
        except:
            print("Both images are not available yet !")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

del pipeline