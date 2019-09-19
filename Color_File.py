# Module defines one class Color_File() that handles writing to and reading from
# the color.csv file.

import Color as color

class Color_File():
    __def_name = "colors.csv"
    __colors = [] # list of color objects, each object stores hsv min
    # and max values, as well as exclusivity and the color name as a string
    __color_names = [] # list of only the color names

    def __init__(self):
        self.read_csv()

    def get_color_names(self, color_names):
        # del color_names[:]
        for x in range(len(self.__color_names)):
            color_names.append(self.__color_names[x])

    def read_csv(self):
        # method reads the colors.csv file into local variables

        # delete current color data
        del self.__colors[:]
        del self.__color_names[:]

        # open colors.csv
        csv_file = self.__def_name
        file = open(csv_file,"r")

        # read color label, exclusivity, hsv min, and hsv max values from color
        # file and store data in local vars
        for line in file:
            line = line.strip()
            csv_line = line.split(",")
            name = csv_line[0]
            hsv_min = [int(csv_line[1]), int(csv_line[2]), int(csv_line[3])]
            hsv_max = [int(csv_line[4]), int(csv_line[5]), int(csv_line[6])]

            exclusive = None
            if csv_line[7] == "FALSE":
                exclusive = False

            elif csv_line[7] == "TRUE":
                exclusive = True

            self.__color_names.append(name)
            new_Obj = color.Color(name, hsv_min, hsv_max, exclusive)
            self.__colors.append(new_Obj)

        file.close()

    def write_csv(self):
        # method writes contents of self.__colors[] into the colors.csv file
        csv_file = self.__def_name
        file = open(csv_file, "w")
        for x in range(len(self.__color_names)):
            hsv_min = self.__colors[x].get_hsv_MIN()
            hsv_max = self.__colors[x].get_hsv_MAX()
            name_str = self.__colors[x].get_color_name()
            exclusive_str = "FALSE"
            if self.__colors[x].is_exclusive():
                exclusive_str = "TRUE"

            file.write(name_str)
            file.write(",")

            for y in range(3):
                file.write(str(hsv_min[y]))
                file.write(",")

            for y in range(3):
                file.write(str(hsv_max[y]))
                file.write(",")

            file.write(exclusive_str)
            file.write(",")
            file.write("\n")

        file.close()

    def get_entry_text(self, color):
        # Method returns a string displaying the contents of the csv file for the
        # specified color. Used to display memory contents in the color
        # configuration gui.
        cn = None
        text = ""
        for x in range(len(self.__color_names)):
            if color == self.__color_names[x]:
                cn = x
                break
        min_string = str(self.__colors[cn].get_hsv_MIN())
        max_string = str(self.__colors[cn].get_hsv_MAX())
        exclusive_string = str(self.__colors[cn].is_exclusive())
        text = min_string+';'+max_string+';'+exclusive_string
        return text

    def write_to_color(self, color, hsv_MIN, hsv_MAX, exclusive):
        # method writes over the specified color with the given data
        cn = None
        for x in range(len(self.__color_names)):
            if color == self.__color_names[x]:
                cn = x

        self.__colors[cn].set_values(color, hsv_MIN, hsv_MAX, exclusive)


    def get_hsv_MIN(self, color):
        # method returns the hsv_Min for the specified color
        cn = None
        for x in range(len(self.__color_names)):
            if color == self.__color_names[x]:
                cn = x

        return self.__colors[cn].get_hsv_MIN()

    def get_hsv_MAX(self, color):
        # method returns the hsv_Max for the specified color
        cn = None
        for x in range(len(self.__color_names)):
            if color == self.__color_names[x]:
                cn = x

        return self.__colors[cn].get_hsv_MAX()

    def is_exclusive(self, color):
        # method returns the exclusivity of the specified color
        cn = None
        for x in range(len(self.__color_names)):
            if color == self.__color_names[x]:
                cn = x

        return self.__colors[cn].is_exclusive()

