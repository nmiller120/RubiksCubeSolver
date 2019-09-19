# Module defines a single class Mask. This class performs color filtering
# on a given image. It also provides a mask (as defined by openCV), which is a
# 2d array that represents the image with each pixel that satisfied the filter
# criteria having a value of 255 and each pixel not passing the filter criteria
# having a value of 0.

import cv2 # computer vision library for working with image processing
import numpy as np # library of advanced math tools used by openCV
import Color as color # color filter object


class Mask():
    __lower = None # lower hsv
    __upper = None # upper hsv
    __exclusive = None # exclusive / inclusive color range
    __color_name = None # color that the mask is attempting to detect in the image


    def __init__(self, name = None, lower_array = None, upper_array = None, exclusive = None):
        # initialize default Mask parameters
        self.__color_name = name
        self.__lower = lower_array
        self.__upper = upper_array
        self.__exclusive = exclusive

    def get_mask(self, sourceImage, lower_array = None, upper_array = None, exclusive = None):
        # method returns a image mask as a numpy array. If a given pixel falls in
        # the filter criteria it is given the value of 255, if it falls outside
        # the criteria it is given the value of 0.

        # if filter criteria is not provided, use defaults
        if lower_array == None:
            lower_array = self.__lower
            upper_array = self.__upper
            exclusive = self.__exclusive

        # source image is provided as a 2 dimensional numpy array with each element
        # being a list of the given pixels in RGB, this invocation of the cvtColor()
        # method returns the image coded in HSV
        hsv = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2HSV)

        # if we are using an exclusive range, filter hue values outside given range
        if exclusive:
            hue_low = [lower_array[0], 0, 0]
            hue_high = [upper_array[0], 255, 255]
            sv_mask = cv2.inRange(hsv, np.array([0,lower_array[1],lower_array[2]]), np.array([255,upper_array[1],upper_array[2]]))
            hue_mask_inv = cv2.inRange(hsv, np.array(hue_low), np.array(hue_high))
            hue_mask = cv2.bitwise_not(hue_mask_inv)
            mask = cv2.bitwise_and(sv_mask, hue_mask)

        # if we are using an inclusive range, filter hue values inside the given
        # range
        else:
            mask = cv2.inRange(hsv, np.array(lower_array), np.array(upper_array))

        # return a mask of the image, with pixels passing the filter being white
        # and pixels failing the filter criteria being black
        return mask

    def parse_cap(self, sourceImage, lower_array, upper_array, exclusive):
            # method returns pixels inside the filtering criteria as their normal
            # color and pixels outside the filtering criteria as black
            mask = self.get_mask(sourceImage, lower_array, upper_array, exclusive)
            res = cv2.bitwise_and(sourceImage, sourceImage, mask=mask)
            return res

