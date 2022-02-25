"""
Model is a module with a Model class that contains all application essential
data (only data). Extra `Property` class is used for ability to bind data with
each other and with widgets.

Development notes:
    To add a new data property:
    1) Mention it inside `Model._init_properties` function as Property.
    2) Add setter and getter of this property.

Author: Artem Shepelin
License: GPLv3
"""

import os

import matplotlib.pyplot
import numpy as np
from PyQt6.QtCore import pyqtSignal as Signal

import gleipnir.utils.colormaps as cmap
from gleipnir.utils.property import Property


class Model:
    def __init__(self):
        super().__init__()
        self._init_properties()


    def _init_properties(self):
        cmap.add_viewer_standard_colormap()
        self._colormaps = matplotlib.pyplot.colormaps()

        self._axes_color = Property("#344291")
        self._axes_labels_color = Property("#4e63e3")
        self._background_color = Property("#0f1016")
        self._center_lines_color = Property("#344291")
        self._colormap = Property("CMRmap")
        self._data = Property(None)
        self._dpi = Property(100)
        self._figsize = Property((6, 6))
        self._frame_color = Property("#0f1016")
        self._input_file = Property("")
        self._is_background_transparent = Property(True)
        self._is_center_lines_displayed = Property(True)
        self._is_show_frame = Property(False)
        self._output_file = Property("")
        self._ticks_color = Property("#4e63e3")
        self._title = Property("Title")
        self._title_color = Property("#4e63e3")
        self._v_max = Property(0.2)
        self._v_min = Property(0.0)
        self._x_axis_name = Property("X Axis Name")
        self._y_axis_name = Property("Y Axis Name")

        self.data.changed.connect(self._on_file_open)


    @property
    def axes_color(self):
        return self._axes_color


    @axes_color.setter
    def axes_color(self, value):
        self._axes_color.setValue(value)


    @property
    def axes_labels_color(self):
        return self._axes_labels_color


    @axes_labels_color.setter
    def axes_labels_color(self, value):
        self._axes_labels_color.setValue(value)


    @property
    def background_color(self):
        return self._background_color


    @background_color.setter
    def background_color(self, value):
        self._background_color.setValue(value)


    @property
    def center_lines_color(self):
        return self._center_lines_color


    @center_lines_color.setter
    def center_lines_color(self, value):
        self._center_lines_color.setValue(value)


    @property
    def colormap(self):
        return self._colormap


    @colormap.setter
    def colormap(self, value):
        self._colormap.setValue(value)


    @property
    def colormaps(self):
        return self._colormaps


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, file_path):
        if self.input_file.value != file_path:
            self.input_file = file_path
        if os.path.exists(file_path):
            f = open(file_path, "r")
            f_list = f.read().split("\n")
            f.close()

            get_parameter = lambda lst, i: lst[i].split(" ")[-1]
            get_int = lambda lst, i: int(get_parameter(lst, i))
            get_float = lambda lst, i: float(get_parameter(lst, i))

            try:
                nR = get_int(f_list, 0)
                nZ = get_int(f_list, 1)
                dr = get_float(f_list, 2)
                dz = get_float(f_list, 3)
                r0 = get_float(f_list, 4)
                z0 = get_float(f_list, 5)
                V1 = get_float(f_list, 6)
                V2 = get_float(f_list, 7)
                dV = get_float(f_list, 8)
                Incl = get_float(f_list, 9)
                ENA = get_float(f_list, 10)
                Coeff = get_float(f_list, 11)

                AbsPlot = np.array([float(i) for i in f_list[-2].split(" ")[:-1]])
                AbsPlot = AbsPlot[::-1].reshape(nR + 1, nZ + 1).T
                AbsPlot[AbsPlot == 0] = None # Set all 0 values to None

                input_data = {
                    "nR": nR,
                    "nZ": nZ,
                    "dr": dr,
                    "dz": dz,
                    "r0": r0,
                    "z0": z0,
                    "V1": V1,
                    "V2": V2,
                    "dV": dV,
                    "Incl": Incl,
                    "ENA": ENA,
                    "Coeff": Coeff,
                    "AbsPlot": AbsPlot}

                self._data.setValue(input_data)
            except:
                raise Exception # Invalid File Format
                return
        else:
            raise FileNotFoundError


    def data_write(self, file_path, figure):
        if self.output_file.value != file_path:
            self.output_file = file_path
        figure.savefig(self.output_file.value, dpi=self.dpi.value,
                       transparent=self.is_background_transparent.value)


    @property
    def dpi(self):
        return self._dpi


    @dpi.setter
    def dpi(self, value):
        self._dpi.setValue(value)


    @property
    def figsize(self):
        return self._figsize


    @figsize.setter
    def figsize(self, value):
        self._figsize.setValue(value)


    @property
    def frame_color(self):
        return self._frame_color


    @frame_color.setter
    def frame_color(self, value):
        self._frame_color.setValue(value)


    @property
    def input_file(self):
        return self._input_file


    @input_file.setter
    def input_file(self, value):
        self._input_file.setValue(value)


    @property
    def is_background_transparent(self):
        return self._is_background_transparent


    @is_background_transparent.setter
    def is_background_transparent(self, value):
        self._is_background_transparent.setValue(value)


    @property
    def is_center_lines_displayed(self):
        return self._is_center_lines_displayed


    @is_center_lines_displayed.setter
    def is_center_lines_displayed(self, value):
        self._is_center_lines_displayed.setValue(value)


    @property
    def is_show_frame(self):
        return self._is_show_frame


    @is_show_frame.setter
    def is_show_frame(self, value):
        self._is_show_frame.setValue(value)


    @property
    def output_file(self):
        return self._output_file


    @output_file.setter
    def output_file(self, value):
        self._output_file.setValue(value)


    @property
    def ticks_color(self):
        return self._ticks_color


    @ticks_color.setter
    def ticks_color(self, value):
        self._ticks_color.setValue(value)


    @property
    def title(self):
        return self._title


    @title.setter
    def title(self, value):
        self._title.setValue(value)


    @property
    def title_color(self):
        return self._title_color


    @title_color.setter
    def title_color(self, value):
        self._title_color.setValue(value)


    @property
    def v_max(self):
        return self._v_max


    @v_max.setter
    def v_max(self, value):
        self._v_max.setValue(value)


    @property
    def v_min(self):
        return self._v_min


    @v_min.setter
    def v_min(self, value):
        self._v_min.setValue(value)


    @property
    def x_axis_name(self):
        return self._x_axis_name


    @x_axis_name.setter
    def x_axis_name(self, value):
        self._x_axis_name.setValue(value)


    @property
    def y_axis_name(self):
        return self._y_axis_name


    @y_axis_name.setter
    def y_axis_name(self, value):
        self._y_axis_name.setValue(value)


    def _on_file_open(self):
        path_head, path_tail = os.path.split(self.input_file.value)
        name, ext = os.path.splitext(path_tail)
        self.output_file = os.path.join(path_head, name + ".png")