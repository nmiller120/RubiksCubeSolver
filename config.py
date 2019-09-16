import Objects_GUI as gui
import Objects_File as files
import Objects_Color as color
import Objects_Overlay as overlay

from Tkinter import *
import numpy as np
import cv2


frame_resolution = [0,0]
##overlay_width = 0
##overlay_top_left = [0,0]
colors = []
##black_image = None
##white_image = None

def add_color(color_object):
    colors.append(color_object)

def set_resolution(bgr_image):
    global black_image
    global white_image

    del frame_resolution[:]
    grayscale_image = cv2.cvtColor(np.copy(bgr_image), cv2.COLOR_BGR2GRAY)
    _resolution_list = list(grayscale_image.shape)

    hold = _resolution_list[1]
    _resolution_list[1] = _resolution_list[0]
    _resolution_list[0] = hold

    for x in range(2):
        frame_resolution.append(_resolution_list[x])

    black_image = np.zeros((frame_resolution[1], frame_resolution[0]))
    white_image = black_image + 255
