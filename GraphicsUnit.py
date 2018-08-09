def scatter_plot_map(coordinates, ax):
    for coord in coordinates:
        ax.scatter(coord[0], coord[1])


def connect_points(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], c="black", lw=0.75, ls="dashed")


def plot_connection(ax, connection):
    ax.plot([connection[0][0], connection[1][0]], [connection[0][1], connection[1][1]], c="black", lw=0.75, ls="dashed")


def draw_node_based(ax, nodes):
    for ind, node in enumerate(nodes):
        if not ind == len(nodes)-1:
            connect_points(ax, node[0], node[1], nodes[ind + 1][0], nodes[ind + 1][1])
        elif ind == len(nodes)-1:
            connect_points(ax, node[0], node[1], nodes[0][0], nodes[0][1])

