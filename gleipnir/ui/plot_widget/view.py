"""
PlotWidget View is a view class for Matplotlib plot widget.

Author: Artem Shepelin
License: GPLv3
"""

import matplotlib as mpl
mpl.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import mpl_toolkits.axes_grid1
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea
import numpy as np
from PyQt6.QtGui import QColor


class PlotWidget(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self._dpi = 100
        if "dpi" in kwargs.keys():
            self._dpi = kwargs["dpi"]
        self._figsize = (6, 6)
        if "figsize" in kwargs.keys():
            self._figsize = kwargs["figsize"]

        self.figure = Figure(figsize=self._figsize, dpi=self._dpi)
        self.ax = self.figure.add_subplot(1, 1, 1)

        super().__init__(self.figure)

        self.setFixedSize(self._dpi * self._figsize[0],
                          self._dpi * self._figsize[1])

        self._axes_color = None
        self._axes_labels_color = None
        self._background_color = None
        self._center_lines_color = None
        self._colormap = None
        self._data = None
        self._frame_color = None
        self._is_background_transparent = None
        self._is_center_lines_displayed = None
        self._is_show_frame = None
        self._ticks_color = None
        self._title = None
        self._title_color = None
        self._v_max = None
        self._v_min = None
        self._x_axis_name = None
        self._y_axis_name = None


    def setAxesColor(self, axes_color):
        if self._axes_color != axes_color:
            self._axes_color = axes_color
            self._draw_axes_color()
            self.draw()


    def setAxesLabelsColor(self, axes_labels_color):
        if self._axes_labels_color != axes_labels_color:
            self._axes_labels_color = axes_labels_color
            self._draw_axes_labels_color()
            self.draw()


    def setBackgroundColor(self, background_color):
        if self._background_color != background_color:
            self._background_color = background_color
            self._draw_background()
            self.draw()


    def setCenterLinesColor(self, center_lines_color):
        if self._center_lines_color != center_lines_color:
            self._clear()
            self._center_lines_color = center_lines_color
            self._draw_full()


    def setColormap(self, colormap):
        if self._colormap != colormap:
            self._clear()
            self._colormap = colormap
            self._draw_full()


    def setData(self, data):
        if self._data != data:
            self._clear()
            self._data = data
            self._draw_full()


    def setDpi(self, dpi):
        if self._dpi != dpi:
            self._dpi = dpi
            self._reset()


    def setFrameColor(self, frame_color):
        if self._frame_color != frame_color:
            self._clear()
            self._frame_color = frame_color
            self._draw_full()


    def setIsBackgroundTransparent(self, is_background_transparent):
        if self._is_background_transparent != is_background_transparent:
            self._is_background_transparent = is_background_transparent
            self._draw_background()
            self.draw()


    def setIsCenterLinesDisplayed(self, is_center_lines_displayed):
        if self._is_center_lines_displayed != is_center_lines_displayed:
            self._clear()
            self._is_center_lines_displayed = is_center_lines_displayed
            self._draw_full()


    def setIsShowFrame(self, is_show_frame):
        if self._is_show_frame != is_show_frame:
            self._clear()
            self._is_show_frame = is_show_frame
            self._draw_full()


    def setTicksColor(self, ticks_color):
        if self._ticks_color != ticks_color:
            self._ticks_color = ticks_color
            self._draw_ticks_color()
            self.draw()


    def setTitle(self, title):
        if self._title != title:
            self._title = title
            try:
                self._draw_title()
                self.draw()
            except:
                pass


    def setTitleColor(self, title_color):
        if self._title_color != title_color:
            self._title_color = title_color
            self._draw_title_color()
            self.draw()


    def setVMax(self, v_max):
        if self._v_max != v_max:
            self._clear()
            self._v_max = v_max
            self._draw_full()


    def setVMin(self, v_min):
        if self._v_min != v_min:
            self._clear()
            self._v_min = v_min
            self._draw_full()


    def setXAxisName(self, x_axis_name):
        if self._x_axis_name != x_axis_name:
            self._x_axis_name = x_axis_name
            try:
                self._draw_x_axis_name()
                self.draw()
            except:
                pass


    def setYAxisName(self, y_axis_name):
        if self._y_axis_name != y_axis_name:
            self._y_axis_name = y_axis_name
            try:
                self._draw_y_axis_name()
                self.draw()
            except:
                pass


    def _clear(self):
        self.ax.clear()


    def _draw_axes_color(self):
        if self._axes_color:
            for axes in self.figure.axes:
                for spines in axes.spines.keys():
                    axes.spines[spines].set_color(self._axes_color)


    def _draw_axes_labels_color(self):
        if self._axes_labels_color:
            self.ax.xaxis.label.set_color(self._axes_labels_color)
            self.ax.yaxis.label.set_color(self._axes_labels_color)


    def _draw_background(self):
        self.figure.patch.set_facecolor(self._background_color)
        if self._is_background_transparent:
            self.ax.patch.set_alpha(0)
        else:
            self.figure.patch.set_alpha(1)
            self.ax.patch.set_facecolor(self._background_color)
            self.ax.patch.set_alpha(1)


    def _draw_center_lines(self):
        if self._is_center_lines_displayed:
            props = {"xycoords": "axes fraction", "textcoords": "axes fraction",
                     "arrowprops": {"color": self._center_lines_color,
                     "arrowstyle": "-", "connectionstyle": "arc3"}}
            self.ax.annotate("", xy=(0, 0.5), xytext=(1, 0.5), **props)
            self.ax.annotate("", xy=(0.5, 0), xytext=(0.5, 1), **props)


    def _draw_frame(self):
        if self._data and self._is_show_frame:
            # circle frame
            ada = AnchoredDrawingArea(0, 0, 0, 0, loc='center', pad=0.)
            c = Circle((0, 0), 154, fill=False,
                       edgecolor=self._frame_color, linewidth=5)
            ada.drawing_area.add_artist(c)
            self.ax.add_artist(ada)


    def _draw_full(self):
        self._draw_axes_color()
        self._draw_axes_labels_color()
        self._draw_background()
        self._draw_center_lines()
        self._draw_frame()
        self._draw_image()
        self._draw_ticks_color()
        self._draw_title()
        self._draw_title_color()
        self._draw_x_axis_name()
        self._draw_y_axis_name()
        self.draw()


    def _draw_image(self):
        if self._data:
            r0 = self._data["r0"]
            nR = self._data["nR"]
            dr = self._data["dr"]
            z0 = self._data["z0"]
            nZ = self._data["nZ"]
            dz = self._data["dz"]
            V1 = self._data["V1"]
            V2 = self._data["V2"]
            dV = self._data["dV"]

            r = np.arange(r0, r0 + (nR + 1) * dr, dr)
            z = np.arange(z0, z0 + (nZ + 1) * dz, dz)
            v = np.arange(V1, V2 + dV, dV)

            im = self.ax.imshow(self._data["AbsPlot"], cmap=self._colormap,
                                vmin=self._v_min, vmax=self._v_max)
            if len(self.figure.axes) > 1: # remove old colorbar
                [cb.remove() for cb in self.figure.axes[1:]]
            self.figure.colorbar(
                im,
                cax=mpl_toolkits.axes_grid1.make_axes_locatable(self.ax)
                    .append_axes("right", size="5%", pad=0.05))
            self.ax.set_xticks(np.arange(0, nR + nR / 4, nR / 4))
            self.ax.set_yticks(np.arange(0, nZ + nZ / 4, nZ / 4))
            self.ax.set_xticklabels(np.arange(r[0], r[-1] + (r[-1] - r[0]) / 4,
                                              (r[-1] - r[0]) / 4))
            self.ax.set_yticklabels(np.arange(z[0], z[-1] + (z[-1] - z[0]) / 4,
                                              (z[-1] - z[0]) / 4)[::-1])

            # cut border pixels
            patch = Circle((nR // 2, nZ // 2), radius=47,
                           transform=self.ax.transData)
            im.set_clip_path(patch)


    def _draw_ticks_color(self):
        if self._ticks_color:
            for axes in self.figure.axes:
                axes.tick_params(axis="x", colors=self._ticks_color)
                axes.tick_params(axis="y", colors=self._ticks_color)


    def _draw_title(self):
        self.ax.set_title(self._title, fontsize=14)


    def _draw_title_color(self):
        if self._title_color:
            self.ax.title.set_color(self._title_color)


    def _draw_x_axis_name(self):
        self.ax.set_xlabel(self._x_axis_name, fontsize=14)


    def _draw_y_axis_name(self):
        self.ax.set_ylabel(self._y_axis_name, fontsize=14)


    def _reset(self):
        self.figure = Figure(figsize=self._figsize, dpi=self._dpi)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.setFixedSize(self._dpi * self._figsize[0],
                          self._dpi * self._figsize[1])
        self._draw_full()