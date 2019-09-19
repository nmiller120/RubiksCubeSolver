# This module contains the code to set up the gui for the Color and Servomotor calibration
# windows.

from tkinter import * # tkinter provides an api to build the gui
import Objects_File as files # module is used by the Setup_Color_Window class to
# access color data file

class Setup_Servo_Window(Frame):
    # gui to calibrate the position of the servomotors. Just displays 8 sliders
    # with accessable data. That data is to be written on the serial port to the
    # servo assembly.

    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_widgets()
        self.grid()

    def create_widgets(self):
        # places the widgets on the gui frame
        self.scale_widgets = []
        for x in range(8):
            text = "Servo " + str(x)
            new_scale = Scale(self, from_=0, to=180, orient=HORIZONTAL, length=250, label = text)
            self.scale_widgets.append(new_scale)
            self.scale_widgets[x].grid(row = x)


class Setup_Color_Window(Frame):
    # this class defines the layout of the color calibration window.

    file_control = None # instance of Color_File
    __complete = False  # bit goes high when user ends calibration session
    __exclusive = None # makes color filter in the display use an exclusive range
    # for the hue
    __color_names = [] # list of colors as a string

    color_entries = [] # list of tkinter Entry widgets, displays the stored data
    # for the given color
    color_set_button = [] # list of tkinter Button widgets, displays a button labeled
    # set to "set" the given color
    color_show_button = [] # list of tkinter Button widgets, displays a button labeled
    # show to "show" the given color
    color_label = [] # list of tkinter Label widgets, just displays a string to label
    # the given color


    def __init__(self, master):
        Frame.__init__(self, master)
        self.__exclusive = BooleanVar()
        self.file_control = files.Color_File()
        self.file_control.get_color_names(self.__color_names)
        self.create_widgets()
        self.grid()


    def create_widgets(self):
        # method adds widgets to gui frame

        #Scales to adjust the hsv mins and maxes for the display
        self.hue_MIN = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)
        self.hue_MAX = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)
        self.sat_MIN = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)
        self.sat_MAX = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)
        self.val_MIN = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)
        self.val_MAX = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=250)


        # populate the frame with widgets to control and view each color
        for x in range(len(self.__color_names)):
            name = self.__color_names[x]
            text = self.file_control.get_entry_text(name)

            new_entry = Entry(self, width=30)
            new_entry.insert(0, text)
            new_entry.config(state=DISABLED)
            self.color_entries.append(new_entry)

            new_set_button = Button(self, text="Set", width=5)
            self.color_set_button.append(new_set_button)

            new_show_button = Button(self, text="Show", width=5)
            self.color_show_button.append(new_show_button)

            new_color_label = Label(self, text=name)
            self.color_label.append(new_color_label)


        # had issues assigning event handlers to these buttons in the above for loop
        self.color_show_button[0].config(command = lambda: self.show_filter(self.__color_names[0]))
        self.color_show_button[1].config(command = lambda: self.show_filter(self.__color_names[1]))
        self.color_show_button[2].config(command = lambda: self.show_filter(self.__color_names[2]))
        self.color_show_button[3].config(command = lambda: self.show_filter(self.__color_names[3]))
        self.color_show_button[4].config(command = lambda: self.show_filter(self.__color_names[4]))
        self.color_show_button[5].config(command = lambda: self.show_filter(self.__color_names[5]))
        self.color_show_button[6].config(command = lambda: self.show_filter(self.__color_names[6]))
        self.color_show_button[7].config(command = lambda: self.show_filter(self.__color_names[7]))

        self.color_set_button[0].config(command = lambda: self.set_filter(self.__color_names[0]))
        self.color_set_button[1].config(command = lambda: self.set_filter(self.__color_names[1]))
        self.color_set_button[2].config(command = lambda: self.set_filter(self.__color_names[2]))
        self.color_set_button[3].config(command = lambda: self.set_filter(self.__color_names[3]))
        self.color_set_button[4].config(command = lambda: self.set_filter(self.__color_names[4]))
        self.color_set_button[5].config(command = lambda: self.set_filter(self.__color_names[5]))
        self.color_set_button[6].config(command = lambda: self.set_filter(self.__color_names[6]))
        self.color_set_button[7].config(command = lambda: self.set_filter(self.__color_names[7]))

        # init Load, Save, and finish buttons and assign event handlers
        self.reset_button = Button(self, text="Reset", command=self.reset_values)
        self.load_defaults_button = Button(self, text="Load Defaults", command=self.load_defaults)
        self.save_defaults_button = Button(self, text="Save Defaults", command=self.save_defaults)
        self.finish_button = Button(self, text='Finish', command=self.finish_setup)

        # init exclusivity checkbox
        self.check_button_label = Label(self, text="Exclusive:")
        self.check_button = Checkbutton(self, variable=self.__exclusive)

        # init labels
        self.hue_label = Label(self, text="Hue:")
        self.sat_label = Label(self, text="Saturation:")
        self.val_label = Label(self, text="Value:")

        self.max_label = Label(self, text="Maximum")
        self.min_label = Label(self, text="Minimum")

        #set scales
        self.hue_MAX.set(255)
        self.sat_MAX.set(255)
        self.val_MAX.set(255)

        # The rest of the code in this method defines the layout of the widgets
        # on the gui
        self.hue_label.grid(row=1, column=0)
        self.sat_label.grid(row=2, column=0)
        self.val_label.grid(row=3, column=0)
        self.max_label.grid(row=0, column=2, columnspan=2)
        self.min_label.grid(row=0, column=1)

        self.hue_MIN.grid(row=1, column=1)
        self.hue_MAX.grid(row=1, column=2, columnspan=2)
        self.sat_MIN.grid(row=2, column=1)
        self.sat_MAX.grid(row=2, column=2, columnspan=2)
        self.val_MIN.grid(row=3, column=1)
        self.val_MAX.grid(row=3, column=2, columnspan=2)

        self.check_button.grid(row=4, column=3)
        self.check_button_label.grid(row=4, column=2)

        length = len(self.__color_names)
        last_row = length+5
        for x in range(length):
            new_x = x+5
            self.color_label[x].grid(row=new_x, column=0)
            self.color_entries[x].grid(row=new_x, column=1)
            self.color_set_button[x].grid(row=new_x, column=2)
            self.color_show_button[x].grid(row=new_x, column=3)

        self.reset_button.grid(row=last_row, column=0)
        self.load_defaults_button.grid(row=last_row, column=1)
        self.save_defaults_button.grid(row=last_row, column=2)
        self.finish_button.grid(row=last_row, column=3)


    def set_filter(self, name):
        # method pulls the current data from the HSV min and max sliders and
        # writes that data to the file_control object for the given color.
        # Note: changes are NOT saved to file unless the save_defaults() method
        # is invoked.
        hsv_MIN = []
        hsv_MIN.append(self.hue_MIN.get())
        hsv_MIN.append(self.sat_MIN.get())
        hsv_MIN.append(self.val_MIN.get())

        hsv_MAX = []
        hsv_MAX.append(self.hue_MAX.get())
        hsv_MAX.append(self.sat_MAX.get())
        hsv_MAX.append(self.val_MAX.get())

        exclusive = self.__exclusive.get()

        self.file_control.write_to_color(name, hsv_MIN, hsv_MAX, exclusive)


        # update the Entry widget for the specified color to reflect changes
        # to memory
        color_number = None
        for x in range(8):
            if self.__color_names[x] == name:
                color_number = x
                break

        text = self.file_control.get_entry_text(name)
        self.color_entries[color_number].config(state=NORMAL)
        self.color_entries[color_number].delete(0, END)
        self.color_entries[color_number].insert(0, text)
        self.color_entries[color_number].config(state=DISABLED)



    def show_filter(self, name):
        # method changes the values of the hsv slider widgets to the values stored
        # in memory for the specified color name.
        hsv_max = self.file_control.get_hsv_MAX(name)
        hsv_min = self.file_control.get_hsv_MIN(name)

        self.hue_MAX.set(hsv_max[0])
        self.sat_MAX.set(hsv_max[1])
        self.val_MAX.set(hsv_max[2])

        self.hue_MIN.set(hsv_min[0])
        self.sat_MIN.set(hsv_min[1])
        self.val_MIN.set(hsv_min[2])

        if self.file_control.is_exclusive(name):
            self.check_button.select()

        elif not self.file_control.is_exclusive(name):
            self.check_button.deselect()

    def reset_values(self):
        # method opens the filter back up and sets the sliders to their max range
        self.hue_MAX.set(255)
        self.hue_MIN.set(0)
        self.sat_MAX.set(255)
        self.sat_MIN.set(0)
        self.val_MAX.set(255)
        self.val_MIN.set(0)


    def save_defaults(self):
        # commits changes to the colors.csv file
        self.file_control.write_csv()

    def load_defaults(self):
        # method clears unsaved color data and reloads color data from hsv file
        self.file_control.read_csv()
        for x in range(len(self.__color_names)):
            text = self.file_control.get_entry_text(self.__color_names[x])
            self.color_entries[x].insert(0, text)


    def finish_setup(self):
        # method closes out the gui, does NOT write to colors.csv. changes must
        # be saved before finishing
        del self.file_control
        self.__complete = True

    def is_complete(self):
        # method returns true if the finish key was pressed and signals that
        # the calibration is complete
        return self.__complete

    def is_exclusive(self):
        # returns true if the current applied filter is using an exclusive range
        # on the hue values
        return self.__exclusive.get()

    def get_lower_range(self):
        # returns the lower hsv values for the current applied filter
        self.min_array = [self.hue_MIN.get(), self.sat_MIN.get(), self.val_MIN.get()]
        return self.min_array

    def get_upper_range(self):
        # returns the upper hsv values for the current applied filter
        self.max_array = [self.hue_MAX.get(), self.sat_MAX.get(), self.val_MAX.get()]
        return self.max_array

##References:
##    http://effbot.org/tkinterbook/scale.htm
