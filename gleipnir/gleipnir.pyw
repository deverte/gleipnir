"""
Gleipnir is a program with graphical user interface for visualizing the results
of modeling the absorption of radiation by stellar and planetary matter.

Compatible file format for parsing (commonly named as "AbsorpPlot.dat"):

    nR <int>
    nZ <int>
    dr <float>
    dz <float>
    r0 <float>
    z0 <float>
    V1 <float>
    V2 <float>
    dV <float>
    Incl <float>
    ENA <float>
    Coeff <float>
    arrays
    AbsPlot
    <float values from 0.0 to 1.0 with size (nR + 1) x (nZ + 1),
     each value separated by space>
    <empty string>

Author: Artem Shepelin
License: MIT
Repository: https://github.com/deverte/gleipnir
"""

__version__ = '0.1.0'

import math
import os
import tkinter as tk
import tkinter.colorchooser
import tkinter.ttk

import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.backends.backend_tkagg
import matplotlib.figure
import matplotlib.pyplot
import mpl_toolkits.axes_grid1

def parse_absorption_plot(filepath):
    f = open(filepath, "r")
    f_list = f.read().split("\n")

    get_parameter = lambda lst, i: lst[i].split(" ")[-1]
    get_int = lambda lst, i: int(get_parameter(lst, i))
    get_float = lambda lst, i: float(get_parameter(lst, i))

    try:
        input_data = {}
        input_data["nR"] = get_int(f_list, 0)
        input_data["nZ"] = get_int(f_list, 1)
        input_data["dr"] = get_float(f_list, 2)
        input_data["dz"] = get_float(f_list, 3)
        input_data["r0"] = get_float(f_list, 4)
        input_data["z0"] = get_float(f_list, 5)
        input_data["V1"] = get_float(f_list, 6)
        input_data["V2"] = get_float(f_list, 7)
        input_data["dV"] = get_float(f_list, 8)
        input_data["Incl"] = get_float(f_list, 9)
        input_data["ENA"] = get_float(f_list, 10)
        input_data["Coeff"] = get_float(f_list, 11)

        input_data["AbsPlot"] = [float(i) for i in f_list[-2].split(" ")[:-1]]
        reshape = lambda arr, x, y: [arr[x * i : x * (i + 1)] for i in range(y)]
        rotate = lambda arr: list(zip(*[i[::-1] for i in arr]))
        input_data["AbsPlot"] = rotate(reshape(input_data["AbsPlot"], input_data["nR"] + 1, input_data["nZ"] + 1))
        # Set all 0 values to None
        input_data["AbsPlot"] = [[math.nan if i == 0 else i for i in row] for row in input_data["AbsPlot"]]

        # NumPy version
        # self.input_data["AbsPlot"] = np.array([float(i) for i in f_list[-2].split(" ")[:-1]])
        # self.input_data["AbsPlot"] = self.input_data["AbsPlot"][::-1].reshape(self.input_data["nR"] + 1, self.input_data["nZ"] + 1).T
        # # Set all 0 values to None
        # self.input_data["AbsPlot"][self.input_data["AbsPlot"] == 0] = None
    except:
        return False

    return input_data

def draw_absorption_plot(input_data, ax, figure, colormap="inferno", vmin=0.0,
                         vmax=0.02, title="Planet", x_axis_name="X",
                         y_axis_name="Y", axes_color="#000000",
                         axes_labels_color="#000000",
                         ticks_color="#000000", title_color="#000000",
                         frame_color="#000000", show_center_lines=1,
                         center_lines_color="#000000",
                         is_background_transparent=1,
                         background_color="#ffffff"):
    r0 = input_data["r0"]
    nR = input_data["nR"]
    dr = input_data["dr"]
    z0 = input_data["z0"]
    nZ = input_data["nZ"]
    dz = input_data["dz"]
    V1 = input_data["V1"]
    V2 = input_data["V2"]
    dV = input_data["dV"]

    arange = lambda start, stop, step: [i * step - start for i in range(int((stop - start) / step))]
    r = arange(r0, r0 + (nR + 1) * dr, dr)
    z = arange(z0, z0 + (nZ + 1) * dz, dz)
    v = arange(V1, V2 + dV, dV)

    ax.clear()
    im = ax.imshow(input_data["AbsPlot"], cmap=colormap, vmin=vmin, vmax=vmax)
    if len(figure.axes) > 1: [cb.remove() for cb in figure.axes[1:]] # remove old colorbar
    figure.colorbar(im, cax=mpl_toolkits.axes_grid1.make_axes_locatable(ax).append_axes("right", size="5%", pad=0.05))
    ax.set_xlabel(x_axis_name, fontsize=14)
    ax.set_ylabel(y_axis_name, fontsize=14)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(arange(0, input_data["nR"] + input_data["nR"] / 4, input_data["nR"] / 4))
    ax.set_yticks(arange(0, input_data["nZ"] + input_data["nZ"] / 4, input_data["nZ"] / 4))
    ax.set_xticklabels(arange(r[0], r[-1] + (r[-1] - r[0]) / 4, (r[-1] - r[0]) / 4))
    ax.set_yticklabels(arange(z[0], z[-1] + (z[-1] - z[0]) / 4, (z[-1] - z[0]) / 4)[::-1])
    ax.spines["top"].set_color(axes_color)
    ax.spines["bottom"].set_color(axes_color)
    ax.spines["left"].set_color(axes_color)
    ax.spines["right"].set_color(axes_color)
    ax.xaxis.label.set_color(axes_labels_color)
    ax.yaxis.label.set_color(axes_labels_color)
    ax.tick_params(axis="x", colors=ticks_color)
    ax.tick_params(axis="y", colors=ticks_color)
    ax.title.set_color(title_color)
    figure.axes[-1].spines["top"].set_color(axes_color)
    figure.axes[-1].spines["bottom"].set_color(axes_color)
    figure.axes[-1].spines["left"].set_color(axes_color)
    figure.axes[-1].spines["right"].set_color(axes_color)
    figure.axes[-1].tick_params(axis="x", colors=ticks_color)
    figure.axes[-1].tick_params(axis="y", colors=ticks_color)
    figure.patch.set_facecolor(background_color)
    if is_background_transparent:
        ax.patch.set_alpha(0)
    else:
        figure.patch.set_alpha(1)
        ax.patch.set_facecolor(background_color)
        ax.patch.set_alpha(1)
    # center lines
    if show_center_lines:
        props = {"xycoords": "axes fraction", "textcoords": "axes fraction", "arrowprops": {"color": center_lines_color, "arrowstyle": "-", "connectionstyle": "arc3"}}
        ax.annotate("", xy=(0, 0.5), xytext=(1, 0.5), **props)
        ax.annotate("", xy=(0.5, 0), xytext=(0.5, 1), **props)
        # ax.stem()
    # circle
    ax.plot(input_data["nR"] // 2, input_data["nZ"] // 2, "o", ms=312, mec=frame_color, mfc="none", mew=5)

def save_absorption_plot(filepath, figure, is_background_transparent=True):
    figure.savefig(filepath, dpi=200, transparent=is_background_transparent)

class Application:
    def __init__(self):
        # Widgets
        self.root = tk.Tk()
        self.plot = None
        self.canvas = None
        # Matplotlib
        self.figure = None
        self.ax = None
        # TkVars
        self.is_plot_loaded = tk.IntVar(value=0)
        self.input_filename = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.colormap = tk.StringVar(value="inferno")
        self.title = tk.StringVar(value="Planet Name")
        self.x_axis_name = tk.StringVar(value="X Axis")
        self.y_axis_name = tk.StringVar(value="Y Axis")
        self.vmin = tk.DoubleVar(value=0.0)
        self.vmax = tk.DoubleVar(value=0.02)
        self.axes_color = tk.StringVar(value="#000000")
        self.axes_labels_color = tk.StringVar(value="#000000")
        self.ticks_color = tk.StringVar(value="#000000")
        self.title_color = tk.StringVar(value="#000000")
        self.frame_color = tk.StringVar(value="#000000")
        self.show_center_lines = tk.IntVar(value=1)
        self.center_lines_color = tk.StringVar(value="#000000")
        self.is_background_transparent = tk.IntVar(value=1)
        self.background_color = tk.StringVar(value="#ffffff")
        # Data
        self.input_data = {}

        # Initialization
        self.root.wm_title("Gleipnir")
        self.root.resizable(False, False)

        self.init_menu()
        self.init_top_panel()
        self.init_center_panel()
        self.init_bottom_panel()
        self.init_right_panel()

        # Traces
        self.is_plot_loaded.trace("w", self.control_traces)
        self.colormap_id = None
        self.title_id = None
        self.x_axis_name_id = None
        self.y_axis_name_id = None
        self.vmin_id = None
        self.vmax_id = None
        self.axes_color_id = None
        self.axes_labels_color_id = None
        self.ticks_color_id = None
        self.title_color_id = None
        self.frame_color_id = None
        self.show_center_lines_id = None
        self.center_lines_color_id = None
        self.is_background_transparent_id = None
        self.background_color_id = None

    def init_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.command_open_file_dialog)
        filemenu.add_command(label="Save", command=self.command_save)
        filemenu.add_command(label="Save As...", command=self.command_save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: tk.messagebox.showinfo("About", f"Gleipnir is a program for visualizing the results of modeling the absorption of radiation by stellar and planetary matter.\n\nVersion: {__version__}\nAuthor: Artem Shepelin\nLicense: MIT\nRepository: https://github.com/deverte/gleipnir"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def init_top_panel(self):
        top_panel = tk.ttk.Frame(self.root)
        top_panel.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        input_file_entry = tk.ttk.Entry(top_panel, textvariable=self.input_filename, width=75).grid(row=0, column=0)
        open_button = tk.ttk.Button(top_panel, text="Open", command=self.command_open_file).grid(row=0, column=1)
        open_dialog_button = tk.ttk.Button(top_panel, text="Open...", command=self.command_open_file_dialog).grid(row=0, column=2)

    def init_center_panel(self):
        center_panel = tk.ttk.Frame(self.root)
        center_panel.grid(row=1, column=0, padx=10)

        self.figure = mpl.figure.Figure(figsize=(6, 6), dpi=100)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.canvas = mpl.backends.backend_tkagg.FigureCanvasTkAgg(self.figure, center_panel)
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def init_bottom_panel(self):
        bottom_panel = tk.ttk.Frame(self.root)
        bottom_panel.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        output_file_entry = tk.ttk.Entry(bottom_panel, textvariable=self.output_filename, width=75).grid(row=6, column=0)
        save_button = tk.ttk.Button(bottom_panel, text="Save", command=self.command_save).grid(row=6, column=1)
        save_as_button = tk.ttk.Button(bottom_panel, text="Save as...", command=self.command_save_as).grid(row=6, column=2)

    def validate_vmin(self, input_value):
        if not self.is_plot_loaded.get():
            return False
        try:
            float(input_value)
        except:
            return False
        # flatten = lambda arr: [element for element in sublist for sublist in arr]
        # min_flatten = lambda arr: min([element if element is not math.nan else math.inf for sublist in arr for element in sublist])
        # max_flatten = lambda arr: max([element if element is not math.nan else -math.inf for sublist in arr for element in sublist])
        # min_value = min_flatten(self.input_data["AbsPlot"])
        # max_value = max_flatten(self.input_data["AbsPlot"])
        min_value = 0.0
        max_value = 1.0
        if float(input_value) < min_value or float(input_value) > self.vmax.get():
            return False
        return True

    def validate_vmax(self, input_value):
        if not self.is_plot_loaded.get():
            return False
        try:
            float(input_value)
        except:
            return False
        min_value = 0.0
        max_value = 1.0
        if float(input_value) > max_value or float(input_value) < self.vmin.get():
            return False
        return True

    def init_right_panel(self):
        right_panel = tk.ttk.Frame(self.root)
        right_panel.grid(row=1, column=1, sticky=tk.N)

        tk.ttk.Label(right_panel, text="Colormap").grid(row=0, column=0)
        colormaps_listbox = tk.ttk.Combobox(right_panel, textvariable=self.colormap, values=matplotlib.pyplot.colormaps())
        colormaps_listbox.grid(row=0, column=1)

        tk.ttk.Label(right_panel, text="Title").grid(row=1, column=0)
        title_entry = tk.ttk.Entry(right_panel, textvariable=self.title).grid(row=1, column=1)

        tk.ttk.Label(right_panel, text="X Axis Name").grid(row=2, column=0)
        xaxis_name_entry = tk.ttk.Entry(right_panel, textvariable=self.x_axis_name).grid(row=2, column=1)

        tk.ttk.Label(right_panel, text="Y Axis Name").grid(row=3, column=0)
        yaxis_name_entry = tk.ttk.Entry(right_panel, textvariable=self.y_axis_name).grid(row=3, column=1)

        tk.ttk.Label(right_panel, text="V Min").grid(row=4, column=0)
        vmin_entry = tk.ttk.Entry(right_panel, textvariable=self.vmin, validate="key", validatecommand=(self.root.register(self.validate_vmin), "%P")).grid(row=4, column=1)

        tk.ttk.Label(right_panel, text="V Max").grid(row=5, column=0)
        vmax_entry = tk.ttk.Entry(right_panel, textvariable=self.vmax, validate="key", validatecommand=(self.root.register(self.validate_vmax), "%P")).grid(row=5, column=1)

        tk.ttk.Label(right_panel, text="Axes Color").grid(row=6, column=0)
        axes_color_button = tk.Button(right_panel, bg=self.axes_color.get(), width=18)
        axes_color_button.grid(row=6, column=1)
        axes_color_button.configure(command=lambda: self.change_color(axes_color_button, self.axes_color))

        tk.ttk.Label(right_panel, text="Axes Labels Color").grid(row=7, column=0)
        axes_labels_color_button = tk.Button(right_panel, bg=self.axes_labels_color.get(), width=18)
        axes_labels_color_button.grid(row=7, column=1)
        axes_labels_color_button.configure(command=lambda: self.change_color(axes_labels_color_button, self.axes_labels_color))

        tk.ttk.Label(right_panel, text="Ticks Color").grid(row=8, column=0)
        ticks_color_button = tk.Button(right_panel, bg=self.ticks_color.get(), width=18)
        ticks_color_button.grid(row=8, column=1)
        ticks_color_button.configure(command=lambda: self.change_color(ticks_color_button, self.ticks_color))

        tk.ttk.Label(right_panel, text="Title Color").grid(row=9, column=0)
        title_color_button = tk.Button(right_panel, bg=self.title_color.get(), width=18)
        title_color_button.grid(row=9, column=1)
        title_color_button.configure(command=lambda: self.change_color(title_color_button, self.title_color))

        tk.ttk.Label(right_panel, text="Frame Color").grid(row=10, column=0)
        frame_color_button = tk.Button(right_panel, bg=self.frame_color.get(), width=18)
        frame_color_button.grid(row=10, column=1)
        frame_color_button.configure(command=lambda: self.change_color(frame_color_button, self.frame_color))

        show_center_lines_checkbutton = tk.Checkbutton(right_panel, variable=self.show_center_lines, text="Show Center Lines").grid(row=11, column=0, columnspan=2)

        tk.ttk.Label(right_panel, text="Center Lines Color").grid(row=12, column=0)
        center_lines_color_button = tk.Button(right_panel, bg=self.center_lines_color.get(), width=18)
        center_lines_color_button.grid(row=12, column=1)
        center_lines_color_button.configure(command=lambda: self.change_color(center_lines_color_button, self.center_lines_color))

        is_background_transparent_checkbutton = tk.Checkbutton(right_panel, variable=self.is_background_transparent, text="Transparent Background").grid(row=13, column=0, columnspan=2)

        tk.ttk.Label(right_panel, text="Background Color").grid(row=14, column=0)
        background_color_button = tk.Button(right_panel, bg=self.background_color.get(), width=18)
        background_color_button.grid(row=14, column=1)
        background_color_button.configure(command=lambda: self.change_color(background_color_button, self.background_color))

        for child in right_panel.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky=tk.W)

    def change_color(self, source_button, variable):
        color = tkinter.colorchooser.askcolor()[1]
        source_button.configure(bg=color)
        variable.set(color)

    def open_file(self):
        try:
            self.input_data = parse_absorption_plot(self.input_filename.get())
            if not self.input_data:
                tk.messagebox.showerror("Error", f"Error: file \"{self.input_filename.get()}\" has incompatible format.")
                return
            self.update_plot()
            self.update_output_filename()
            self.is_plot_loaded.set(1)
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"Error: file \"{self.input_filename.get()}\" not found.")

    def command_open_file(self):
        self.open_file()

    def command_open_file_dialog(self):
        self.input_filename.set(tk.filedialog.askopenfilename(title="Select file", filetypes=(("Data files (*.dat)", "*.dat"), ("All files", "*.*"))))
        self.open_file()

    def control_traces(self, *args):
        if self.is_plot_loaded.get():
            self.colormap_id = self.colormap.trace("w", self.update_plot)
            self.title_id = self.title.trace("w", self.update_plot)
            self.x_axis_name_id = self.x_axis_name.trace("w", self.update_plot)
            self.y_axis_name_id = self.y_axis_name.trace("w", self.update_plot)
            self.vmin_id = self.vmin.trace("w", self.update_plot)
            self.vmax_id = self.vmax.trace("w", self.update_plot)
            self.axes_color_id = self.axes_color.trace("w", self.update_plot)
            self.axes_labels_color_id = self.axes_labels_color.trace("w", self.update_plot)
            self.ticks_color_id = self.ticks_color.trace("w", self.update_plot)
            self.title_color_id = self.title_color.trace("w", self.update_plot)
            self.frame_color_id = self.frame_color.trace("w", self.update_plot)
            self.show_center_lines_id = self.show_center_lines.trace("w", self.update_plot)
            self.center_lines_color_id = self.center_lines_color.trace("w", self.update_plot)
            self.is_background_transparent_id = self.is_background_transparent.trace("w", self.update_plot)
            self.background_color_id = self.background_color.trace("w", self.update_plot)
        else:
            self.colormap.trace_vdelete("w", self.colormap_id)
            self.title.trace_vdelete("w", self.title_id)
            self.x_axis_name.trace_vdelete("w", self.x_axis_name_id)
            self.y_axis_name.trace_vdelete("w", self.y_axis_name_id)
            self.vmin.trace_vdelete("w", self.vmin_id)
            self.vmax.trace_vdelete("w", self.vmax_id)
            self.axes_color.trace_vdelete("w", self.axes_color_id)
            self.axes_labels_color.trace_vdelete("w", self.axes_labels_color_id)
            self.ticks_color.trace_vdelete("w", self.ticks_color_id)
            self.title_color.trace_vdelete("w", self.title_color_id)
            self.frame_color.trace_vdelete("w", self.frame_color_id)
            self.show_center_lines.trace_vdelete("w", self.show_center_lines_id)
            self.center_lines_color.trace_vdelete("w", self.center_lines_color_id)
            self.is_background_transparent.trace_vdelete("w", self.is_background_transparent_id)
            self.background_color.trace_vdelete("w", self.background_color_id)

    def update_plot(self, *args):
        draw_absorption_plot(self.input_data, self.ax, self.figure,
                             colormap=self.colormap.get(), vmin=self.vmin.get(),
                             vmax=self.vmax.get(), title=self.title.get(),
                             x_axis_name=self.x_axis_name.get(),
                             y_axis_name=self.y_axis_name.get(),
                             axes_color=self.axes_color.get(),
                             axes_labels_color=self.axes_labels_color.get(),
                             ticks_color=self.ticks_color.get(),
                             title_color=self.title_color.get(),
                             frame_color=self.frame_color.get(),
                             show_center_lines=self.show_center_lines.get(),
                             center_lines_color=self.center_lines_color.get(),
                             is_background_transparent=self.is_background_transparent.get(),
                             background_color=self.background_color.get())
        try:
            self.canvas.draw()
        except:
            pass

    def update_output_filename(self, *args):
        input_filename = self.input_filename.get()
        path_head, path_tail = os.path.split(input_filename)
        file_name, file_ext = os.path.splitext(path_tail)
        self.output_filename.set(os.path.join(path_head, file_name + ".png"))

    def save_plot(self, filename):
        if filename:
            try:
                save_absorption_plot(filename, self.figure, is_background_transparent=self.is_background_transparent.get())
            except Exception:
                tk.messagebox.showerror("Error", f"Error: file \"{self.output_filename.get()}\" can not be saved.")
        else:
            tk.messagebox.showerror("Error", f"Error: file \"{self.output_filename.get()}\" can not be saved.")

    def command_save(self):
        self.save_plot(self.output_filename.get())

    def command_save_as(self):
        ftypes = [(f"{val} (*.{key})", f".{key}") for key, val in self.figure.canvas.get_supported_filetypes().items()]
        new_file = tk.filedialog.asksaveasfile(filetypes=ftypes, defaultextension=".png", title="Select file", initialfile=os.path.split(self.output_filename.get())[1])
        if new_file:
            self.output_filename.set(new_file.name)
            self.save_plot(self.output_filename.get())
        else:
            tk.messagebox.showerror("Error", f"Error: file \"{self.output_filename.get()}\" can not be saved.")

    def exec(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application().exec()