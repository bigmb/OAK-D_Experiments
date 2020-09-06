"""
Description : 
=============

This code is a simple example of how to get started with the depthai API. It shows how to :
1. Initialise the device.
2. Get the data packets from the device. (The bounding box and the rgb frame)
3. Draw the bounding box using the extracted bounding box information on the extracted image from the stream.
4. Display the output

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

out_h,out_w = [400,640]
output_file = "out2.avi"
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
    'camera': {'mono': {'resolution_h': 400, 'fps': 30}},
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
            out = np.zeros((left_frame.shape[0],left_frame.shape[1],3))
            out[:,:,0] = right_frame/255
            out[:,:,1] = right_frame/255
            out[:,:,2] = left_frame/255
            cv2.imshow("3D view",out)
            print(out.shape)
            out_wr.write((out*255).astype(np.uint8))
        except:
            print("Both images are not available yet !")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

out_wr.release()
del pipeline
