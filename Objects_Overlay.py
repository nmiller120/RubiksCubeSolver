import cv2
import numpy as np
import config
import Objects_Color as color


class Mask():
    __lower = None # lower hsv
    __upper = None # upper hsv
    __exclusive = None # exclusive / inclusive color range
    __color_name = None # color that the mask is for
    __gauss = None # gaussian filter object


    def __init__(self, name = None, lower_array = None, upper_array = None, exclusive = None):
        self.__color_name = name 
        self.__lower = lower_array
        self.__upper = upper_array
        self.__exclusive = exclusive
        self.__gauss = GaussianFilter()

    def get_mask(self, capture_obj, lower_array = None, upper_array = None, exclusive = None):
        gauss_filter = False 
        if lower_array == None:
            lower_array = self.__lower
            upper_array = self.__upper
            exclusive = self.__exclusive
            gauss_filter = True


        hsv = cv2.cvtColor(capture_obj, cv2.COLOR_BGR2HSV)

        if exclusive:
            hue_low = [lower_array[0], 0, 0]
            hue_high = [upper_array[0], 255, 255]
            sv_mask = cv2.inRange(hsv, np.array([0,lower_array[1],lower_array[2]]), np.array([255,upper_array[1],upper_array[2]]))
            hue_mask_inv = cv2.inRange(hsv, np.array(hue_low), np.array(hue_high))
            hue_mask = cv2.bitwise_not(hue_mask_inv)
            mask = cv2.bitwise_and(sv_mask, hue_mask)

        else:
            mask = cv2.inRange(hsv, np.array(lower_array), np.array(upper_array))
        if gauss_filter:
            mask = self.__gauss.filter_image(mask)
        return mask

    def parse_cap(self, capture_obj, lower_array, upper_array, exclusive):
            mask = self.get_mask(capture_obj, lower_array, upper_array, exclusive)
            res = cv2.bitwise_and(capture_obj, capture_obj, mask=mask)
            return res


class GaussianFilter():

    def __init__(self):
        pass

    def parse_array(self, boolean_array):
        count = 0
        for arr in boolean_array:
            for val in arr:
                if val != 0:
                    count += 1
        return count > 8

    def get_array(self, img, x, y):
        array = [[img.item(x-1,y-1), img.item(x,y-1), img.item(x+1,y-1)],
        [img.item(x-1,y), img.item(x,y), img.item(x+1,y)],
        [img.item(x-1,y+1), img.item(x,y+1), img.item(x+1,y+1)]]
        return self.parse_array(array)

    def filter_image(self, mask1):
        m,n = mask1.shape
        mask = np.zeros((m, n), np.uint8)

        for i in range(1, m-1):
            for j in range(1, n-1):
                if self.get_array(mask1, i, j):
                    mask.itemset((i,j), 255)

        return mask

