def scatter_plot_map(coordinates, ax):
    """
        Bildet Scatterplot auf einer gegebenen Axe ab
    :param coordinates: Koordinaten
    :param ax: Achse, auf der Koordinaten abgebilden werden sollen
    """
    for coord in coordinates:
        ax.scatter(coord[0], coord[1])


def connect_points(ax, x1, y1, x2, y2):
    """
        Verbinded die Scatter-Plot Punkte
    :param ax: Achse, auf der gezeichnet werden soll
    :param x1: X-Wert der ersten Koordinate
    :param y1: Y-Wert der ersten Koordinate
    :param x2: X-Wert der zweiten Koordinate
    :param y2: Y-Wert der zweiten Koordinate
    :return:
    """
    ax.plot([x1, x2], [y1, y2], c="black", lw=0.75, ls="dashed")


def draw_node_based(ax, nodes):
    """
        Zeichnet alle Verbindungen für eine Liste aus Punkten in der Reihenfolge der Punkte. Wenn ein Punkt der Letzte
        in der Liste ist, wird er mit dem ersten Punkt verbunden.
    :param ax: Die Achse, auf die gezeichnet werden soll
    :param nodes: Eine Liste an Knotenpunkten
    """
    for ind, node in enumerate(nodes):
        if not ind == len(nodes)-1:
            connect_points(ax, node[0], node[1], nodes[ind + 1][0], nodes[ind + 1][1])
        elif ind == len(nodes)-1:
            connect_points(ax, node[0], node[1], nodes[0][0], nodes[0][1])
