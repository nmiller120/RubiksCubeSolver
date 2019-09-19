# Module contains one class Color, which defines filter parameters for a given
# color. HSV refers to the hue, saturation, value color space. If a given pixel
# falls in the hsv range that pixel is given a logical 1, if its outside the pixel
# is assigned a logical 0 when the mask of the image is created. The boolean variable
# exclusive is used for the color red, whose hue values wrap back around (ie. red
# corresponds values less than h ~= 25 and greater than h ~= 240)

class Color():
    __hsv_MAX = [] # maximum hsv value for a given color
    __hsv_MIN = [] # minumum hsv value for a given color
    __exclusive = False # exclusive / inclusive range for a given color
    __color_name = "" # ascii text name of the color

    def __init__(self, color_name, hsv_MIN, hsv_MAX, exclusive):
        self.__hsv_MAX = hsv_MAX
        self.__hsv_MIN = hsv_MIN
        self.__exclusive = exclusive
        self.__color_name = color_name

    def set_values(self, color_name, hsv_MIN, hsv_MAX, exclusive):
        self.__hsv_MAX = hsv_MAX
        self.__hsv_MIN = hsv_MIN
        self.__exclusive = exclusive
        self.__color_name = color_name

    def get_hsv_MAX(self):
        return self.__hsv_MAX

    def get_hsv_MIN(self):
        return self.__hsv_MIN

    def is_exclusive(self):
        return self.__exclusive

    def get_color_name(self):
        return self.__color_name


