import matplotlib.colors

def add_viewer_standard_colormap():
    # red, yellow, green, cyan, blue
    colors = [(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]
    matplotlib.colormaps.register(matplotlib.colors.LinearSegmentedColormap.from_list("ViewerStandard", colors))