import numpy as np
import Objects_File as files
import Objects_Overlay as overlay
import cv2


class FaceReader():
    __file_control = None
    __color_names = []
    __masks = []

    def __init__(self, image):
        # clear color names and color masks arrays
        del self.__color_names[:] 
        del self.__masks[:]
        
        # open color file and get color names
        self.__file_control = files.Color_File()
        self.__file_control.get_color_names(self.__color_names)
        
        # save the image passed as a member var
        self.image = image

        # create color masks
        for x in range(len(self.__color_names)):
            name = self.__color_names[x]
            lower = self.__file_control.get_hsv_MIN(name)
            upper = self.__file_control.get_hsv_MAX(name)
            exclusive = self.__file_control.is_exclusive(name)
            new_mask = overlay.Mask(name, lower, upper, exclusive)
            self.__masks.append(new_mask)
        # 
        self.all_facelets_mask = self.get_all_facelets_mask(image)
        self.get_row_count_array()
        self.get_col_count_array()
        self.parse_arrays()
        self.create_facelet_coord_objects()
        
        # print self.getFaceletColors(image)

    def getFaceletColors(self, image):
        self.all_facelets_mask = self.get_all_facelets_mask(image)
        self.get_row_count_array()
        self.get_col_count_array()
        self.parse_arrays()
        self.create_facelet_coord_objects()
        return self.test_sample_coords()
        
    
    def get_all_facelets_mask(self, image):
        self.mask_array = []
        for i in range(6):
            self.mask_array.append(self.__masks[i].get_mask(image))

        final_mask = cv2.bitwise_or(self.mask_array[0], self.mask_array[1])
        for i in range(2,6):
            final_mask = cv2.bitwise_or(final_mask, self.mask_array[i])

        return final_mask

    def get_row_count_array(self):
        w,h = self.all_facelets_mask.shape
        self.row_count_array = []
        for j in range(0, h):
            row_count = 0
            for i in range(0, w):
                if self.all_facelets_mask.item(i, j) == 255:
                    row_count += 1
            self.row_count_array.append(row_count)

    def get_col_count_array(self):
        w,h = self.all_facelets_mask.shape
        self.col_count_array = []
        for i in range(0, w):
            col_count = 0
            for j in range(0, h):
                if self.all_facelets_mask.item(i, j) == 255:
                    col_count += 1
            self.col_count_array.append(col_count)

    def parse_arrays(self):
        self.row_lines = []
        for i in range(len(self.row_count_array)):
            if self.row_count_array[i] >= 110:
                self.row_lines.append(i)

        self.row_starts = [self.row_lines[0],0,0]
        self.row_ends = [0,0,0]
        current_row = 0

        for i in range(1, len(self.row_lines)-1):
            if self.row_lines[i] - self.row_lines[i-1] <= 4:
                self.row_ends[current_row] = self.row_lines[i]
            else:
                current_row += 1
                self.row_starts[current_row] = self.row_lines[i]

        self.col_lines = []
        for i in range(1, len(self.col_count_array)-1):
            if self.col_count_array[i] >= 90:
                self.col_lines.append(i)

        self.col_starts = [self.col_lines[0],0,0]
        self.col_ends = [0,0,0]
        current_col = 0

        for i in range(1, len(self.col_lines)):
            if self.col_lines[i] - self.col_lines[i-1] == 1:
                self.col_ends[current_col] = self.col_lines[i]
            else:
                current_col += 1
                self.col_starts[current_col] = self.col_lines[i]

    def create_facelet_coord_objects(self):
        self.facelet_coord_objects = []
        for i in range(9):
            current_row = (i%3)
            current_col = (i//3)
            self.facelet_coord_objects.append(
            Facelet_Coords(self.row_starts[current_row], self.row_ends[current_row], self.col_starts[current_col], self.col_ends[current_col])
            )

    def test_sample_coords(self):
        self.colors = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(6):
            color_letter = self.__color_names[i][0]
            for j in range(len(self.colors)):
                if self.facelet_coord_objects[j].sample_coords(self.mask_array[i]) > 2:
                    self.colors[j] = color_letter
        
        return self.colors


class Facelet_Coords():

    def __init__(self, row_start, row_end, col_start, col_end):
        self.sampling_coords = []
        row_offset = int((row_end-row_start)/10)
        col_offset = int((col_end-col_start)/10)

        self.sampling_coords.append((col_start + col_offset, row_start + row_offset)) # Top Left
        self.sampling_coords.append((col_start + col_offset, row_end - row_offset)) # Top Right
        self.sampling_coords.append((col_end - col_offset, row_start + row_offset)) # Bottom Left
        self.sampling_coords.append((col_end - col_offset, row_end - row_offset)) # Bottom Right

    def sample_coords(self, mask):
        count = 0
        for point in self.sampling_coords:
            x,y = point
            if mask.item(x,y) == 255:
                count += 1
        return count
