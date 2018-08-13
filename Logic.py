import math, random

"""Program"""
def load_coordinates_from_file():
    """
        Läd Koordinaten aus der coords.csv
    :return: Gibt die Koordinaten als Liste zurück
    """
    coord_file = "Ressources/coords.csv"
    file = open(coord_file, "r")

    result = []
    for line in file:
        x, y = line.split(";")
        x_clean = float(x)
        y_clean = float(y.strip(r"\n"))

        result.append([x_clean, y_clean])
    return result


def random_route(coordinates):
    """
        Erstellt eine zufällige Route durch alle übergebenen Koordinaten
    :param coordinates:
    :return: Eine zufällige Route durch alle übergebenen Koordinaten
    """
    route = []

    def recurse_route(n):
        for i in range(len(coordinates)):
            route.append(coordinates.pop(random.randrange(len(coordinates))))

        if len(coordinates) > 0:
            recurse_route(n)

    recurse_route(coordinates)
    return route

"""Fitness"""
def distance(node1, node2):
    """
        Berechnet die Distanz zwischen zwei Punkten
    :param node1: Punkt 1
    :param node2: Punkt 2
    :return: Distanz
    """
    return math.sqrt((node1[0]-node2[0])**2 + (node1[1]-node2[1])**2)


def distance_full(route: list):
    """
        Berechnet die Summe aller Teildistanzen einer Route
    :param route: Eine Liste an Punkten (In der Reihenfolge der Route)
    :return: Die Gesamtdistanz der Route
    """
    dist = 0.0
    for ind, node in enumerate(route[:-1]):
        dist += distance(node, route[ind+1])
    dist += distance(route[-1], route[0])  # Connecting last and first node
    return dist

"""Greedy"""
def greedy_algo(coordinates: list, is_first: bool):
    """
        Greedy Algorithmus
    :param coordinates: Koordinaten, für die eine Route gefunden werden soll
    :param is_first: Parameter
    :return: Eine Liste von Koordinaten nach Bearbeitung durch den Greedy Algorithmus
    """
    aux = coordinates
    result = []

    def recurse_route(is_first: bool, **kwargs):
        if is_first:
            c1 = aux.pop(random.randrange(len(aux)))  # random starting point
            result.append(c1)
        else:
            c1 = kwargs["start"]

        distance_temp = 9000  # arbitrary large number to start with
        c2 = None
        c2ind = None
        for ind, coord in enumerate(aux):
            if distance(c1, coord) < distance_temp:
                distance_temp = distance(c1, coord)
                c2 = coord
                c2ind = ind
        result.append(aux.pop(c2ind))

        if len(aux) > 0:
            recurse_route(False, start=c2)

    recurse_route(is_first)
    return result


"""Two Opt Swap"""
def two_opt_swap(route, i, j):
    """
        Tausch von zwei Verbindungen innerhalb einer Route
    :param route: Route auf der operiert wird
    :param i: Startindex
    :param j: Endindex
    :return: Route mit getauschen Punkten
    """
    new = route[:]
    new[i:j] = route[j-1:i-1:-1]
    return new


"""Genetic Algo"""
def swap(route, a, b):
    """
        Tausch zweiter Koordinaten in einer Route
    :param route: Route auf der die Operation ausgeführt wird
    :param a: Koordinate 1
    :param b: Koordinate 2
    :return:
    """
    temp = route[a]
    route[a] = route[b]
    route[b] = temp
    return route


def average_fitness(pop):
    """
        Bildet die durchschnittliche Fitness einer Population
    :param pop: Population aus Routen
    :return: Durchschnittsfitness einer Population
    """
    s = 0.0
    for i in pop:
        s += distance_full(i)
    return s/len(pop)


def genetic_algo_crossover(parrent1: list, parrent2: list):
    """
        Crossover Schema des genetischen Algorithmus
    :param parrent1: Erster Elternteil
    :param parrent2: Zweiter Elternteil
    :return: Offspring Generation Route
    """
    rand_ind1 = random.randrange(0, len(parrent1)-2)

    while True:
        try:  # Catch empty randrange
            rand_ind2 = random.randrange(rand_ind1+1, len(parrent1) - 1)
        except ValueError:
            continue
        break

    offspring1 = [None]*len(parrent1)
    offspring1[rand_ind1:rand_ind2] = parrent1[rand_ind1:rand_ind2]  # Parrent1 slice in offspring

    offspring1_cop = offspring1[:]
    counter = 0
    for i, elem in enumerate(offspring1_cop):
        while offspring1[i] is None:
            if parrent2[counter] not in offspring1:
                offspring1[i] = parrent2[counter]
            counter += 1

    return offspring1


def genetic_algo_random_population(scatter_coordiantes, pop_size):
    """
        Erstellt eine zufällige Population aus Routen für den genetischen Algorithmus
    :param scatter_coordiantes: Koordinaten, die Teil der Route sind
    :param pop_size: Größe der Population / Anzahl der Routen
    :return: Eine Population aus Routen
    """
    pop = []
    for i in range(pop_size):
        pop.append(random_route(scatter_coordiantes[:]))
    return pop
