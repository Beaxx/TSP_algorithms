def scatter_plot_map(coordinates, ax):
    for coord in coordinates:
        ax.scatter(coord[0], coord[1])


def connect_points(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], c="black", lw=0.75, ls="dashed")


def draw_configuration(ax, connections):
    for ind, connection in enumerate(connections):
        if not ind == len(connections)-1:
            connect_points(ax, connection[0], connection[1], connections[ind+1][0], connections[ind+1][1])
        elif ind == len(connections)-1:
            connect_points(ax, connection[0], connection[1], connections[0][0], connections[0][1])
