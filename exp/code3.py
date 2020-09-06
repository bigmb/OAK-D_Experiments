"""
Displaying coloured disparity map

Description : 
=============

This code is a simple example of how to get started with the depthai API. It shows how to :
1. Initialise the device.
2. Read and display the disparity map from the device in color format.

This code can be helpful to get started with experiments involving depth information.
The beauty of OAK-D is that it makes the process of generating the disparity map information super easy.

Useage:
    python3 code3.py
"""

import sys
sys.path.append('/home/pi/depthai/')
import consts.resource_paths
import cv2
import depthai
import numpy as np

device = depthai.Device()

out_h,out_w = [400,640]
output_file = "disparity_color.avi"
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_wr = cv2.VideoWriter(output_file,fourcc,fps,(out_w,out_h))


if not device:
    raise RuntimeError("Error initializing device. Try to reset it.")

pipeline = device.create_pipeline(config={
    'streams': ['left', 'right', 'metaout',{'name': 'disparity_color', 'max_fps': 12.0}],
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
        if packet.stream_name == 'disparity_color':
            disp = packet.getData()
            # disp = (disp - np.min(disp))*1.0/(np.max(disp)-np.min(disp))
            cv2.imshow("disparity map",disp)
            print(disp.shape)
            out_wr.write(disp)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
out_wr.release()
del pipeline