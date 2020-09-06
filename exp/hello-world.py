import numpy as np # numpy - manipulate the packet data returned by depthai
import cv2 # opencv - display the video stream
import depthai # access the camera and its data packets
import consts.resource_paths # load paths to depthai resources

if not depthai.init_device(consts.resource_paths.device_cmd_fpath):
    raise RuntimeError("Error initializing device. Try to reset it.")
