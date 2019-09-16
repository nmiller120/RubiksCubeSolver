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


