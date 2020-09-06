"""
Displaying the left and right camera images

Description : 
=============

This code is a simple example of how to get started with the depthai API. It shows how to :
1. Initialise the device.
2. Read and display left and right images captured from the stereo camera setup.

This code can be helpful to get started with experiments involving stereo camera images.

Useage:
    python3 code2.py
"""

import sys
sys.path.append('/home/pi/depthai/')
import consts.resource_paths
import cv2
import depthai
import numpy as np

device = depthai.Device()
out_h,out_w = [400, 800]
output_file = "left_rightFramesDemo.avi"
fps = 10
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_wr = cv2.VideoWriter(output_file,fourcc,fps,(out_w,out_h))

if not device:
    raise RuntimeError("Error initializing device. Try to reset it.")

pipeline = device.create_pipeline(config={
    'streams': ['left', 'right', 'metaout'],
    'ai': {
        "blob_file": consts.resource_paths.blob_fpath,
        "blob_file_config": consts.resource_paths.blob_config_fpath,
    },
    'camera': {'mono': {'resolution_h': 400, 'fps': 30}}, # or 'camera': {'rgb': {'resolution_h': 1080, 'fps': 30}}, 
})

if pipeline is None:
    raise RuntimeError('Pipeline creation failed!')

left_frame = None
right_frame = None


while True:
    nnet_packets, data_packets = pipeline.get_available_nnet_and_data_packets()
    frame_present = False
    for packet in data_packets:
        if packet.stream_name == 'left':
            left_frame = packet.getData()
            frame_present = True

        elif packet.stream_name == 'right':
            right_frame = packet.getData()
            frame_present = True
        else :
            frame_present = False
    
    if frame_present:
        try:
            out = np.hstack((left_frame,right_frame))
            cv2.imshow("Left and Right Frames",out)
            outimg = np.zeros((out.shape[0],out.shape[1],3))
            outimg[:,:,0] = out
            outimg[:,:,1] = out
            outimg[:,:,2] = out
            out = cv2.resize(outimg,(800,400))
            print(out.shape)
            out_wr.write(out.astype(np.uint8))
        except:
            print("Both images are not available yet !")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

out_wr.release()
del pipeline