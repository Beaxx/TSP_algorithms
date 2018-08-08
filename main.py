import GraphicsUnit as Gu
import matplotlib.pyplot as plt
from matplotlib.pyplot import  plot, draw, show, ion
import math, random
import matplotlib.image as mpimg
import ctypes


def load_coordinates_from_file():
    # Load Coordinates from File
    coord_file = "Ressources/coords.csv"
    file = open(coord_file, "r")

    result = []
    for line in file:
        x, y = line.split(";")
        x_clean = float(x)
        y_clean = float(y.strip(r"\n"))

        result.append([x_clean, y_clean])
    return result


def random_route(nodes):
    aux = nodes
    route = []

    def recurse_route():
        route.append(aux.pop(random.randrange(len(aux))))
        if len(aux) > 0:
            recurse_route()
        else:
            route.append(route[0])  # appending first element last to close circle

    recurse_route()
    return route


def calculate_path_length(connections: list):
    dist = 0.0
    for ind, coord in enumerate(connections[:-1]):
        dist += math.sqrt((coord[0]-connections[ind+1][0])**2 + (coord[1]-connections[ind+1][1])**2)
    return dist


def greedy_algo(coordinates: list, is_first: bool):
    aux = coordinates

    # Get Distance between two points
    def dist(c1, c2):
        return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    result = []

    def recurse_route(is_first: bool, **kwargs):
        if is_first:
            c1 = aux.pop(random.randrange(len(aux)))
            result.append(c1)
        else:
            c1 = kwargs["start"]

        distance_temp = 9000  # arbitrary large number to start with
        c2 = None
        c2ind = None
        for ind, coord in enumerate(aux):
            if dist(c1, coord) < distance_temp:
                distance_temp = dist(c1, coord)
                c2 = coord
                c2ind = ind
        result.append(aux.pop(c2ind))

        if len(aux) > 0:
            recurse_route(False, start=c2)

    recurse_route(is_first)
    return result


def opt_swap_algo(plot_ax, random: list):
    route = random
    best = route
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]  # 2opt swap
                if calculate_path_length(new_route) < calculate_path_length(route):
                    best = new_route
                    improved = True

        plot_ax.clear()
        plt.axis("off")
        img_ax.imshow(img)
        Gu.draw_configuration(plot_ax, best)
        show(block=False)
        plt.pause(0.01)
        route = best
    return best


def sim_annealing(plot_ax, random: list):
    return

"""Initialize Map"""
img = mpimg.imread('Ressources/germany_without_cities.png')  # Map

fig = plt.figure(figsize=(6, 8))
plt.axis("off")
img_ax = fig.add_subplot(111)
img_ax.imshow(img)

scatter_coordianzes = load_coordinates_from_file()  # Scatter
Gu.scatter_plot_map(scatter_coordianzes, img_ax)
show(block=False)
plt.pause(0.01)


"""User Interaction"""
# ctypes.windll.user32.MessageBoxW(0, "Die Software versucht die kürzeste\nVerbinddung zwischen 44 Punkten zu finden.\n\n"
#                                     "Hierzu stehen verschiedene Algorithmen\nbereit, die über das in der Konsole\n"
#                                     "angezeigt Menü gestartet werden können.", "Program Ablauf", 0)
print("Bitte wählen Sie eine Optimierungsalgorithmus:\n"
      "[1]: Greedy - Wählt stets die kürzeste Verbindung zu nächsten Punkt\n"
      "[2]: 2-Opt Swap - Initial zufällige Route, bei der iterativ zwei Routen getauscht werden bis ein (lokales) Optimum erreicht ist\n"
      "[3]: Simulated Annealing - Propabilistische Akzeptanz zu Beginn der Suche gemessen an einem 'hitze' Faktor, der mit der Zeit abnimmt")

algo = int(input())

"""Algorithm Choice"""
if algo == 1:
    greedy_configuration = greedy_algo(scatter_coordianzes, True)
    print("Führe aus: Greedy")
    Gu.draw_configuration(img_ax, greedy_configuration)
    print("Distanz des Pfades: " + str(round(calculate_path_length(greedy_configuration))))
    show()

elif algo == 2:
    scatter_bu = scatter_coordianzes[:]
    random = random_route(scatter_coordianzes)
    Gu.draw_configuration(img_ax, random)
    print("Distanz zu Beginn: " + str(round(calculate_path_length(random))))

    best = opt_swap_algo(img_ax, random)

    print("Distanz abschließend: " + str(round(calculate_path_length(best))))

    img_ax.clear()
    plt.imshow(img)
    plt.axis("off")
    Gu.scatter_plot_map(scatter_bu, fig.add_subplot(111))
    Gu.draw_configuration(img_ax, best)
    show()

elif algo == 3:
    print("Funktion nicht verfügbar")

else:
    print("Falsche Eingabe")
    input()