import GraphicsUnit as Gu
import matplotlib.pyplot as plt
from matplotlib.pyplot import  plot, draw, show, ion
import math, random
import matplotlib.image as mpimg
import ctypes
import itertools
from Logic import *
import copy

"""Initialize Map"""
img = mpimg.imread('Ressources/germany_without_cities.png')  # Map

fig = plt.figure(0, figsize=(6, 8))
plt.suptitle("Best Route")
plt.axis("off")
img_ax = fig.add_subplot(111)
img_ax.imshow(img)

scatter_coordiantes = load_coordinates_from_file()  # Scatter
Gu.scatter_plot_map(scatter_coordiantes, img_ax)
show(block=False)
plt.pause(0.01)

"""User Interaction"""
# ctypes.windll.user32.MessageBoxW(0, "Die Software versucht die kürzeste\nVerbinddung zwischen 44 Punkten zu finden.\n\n"
#                                     "Hierzu stehen verschiedene Algorithmen\nbereit, die über das in der Konsole\n"
#                                     "angezeigt Menü gestartet werden können.", "Program Ablauf", 0)
print("Bitte wählen Sie eine Optimierungsalgorithmus:\n"
      "[1]: Greedy - Wählt stets die kürzeste Verbindung zu nächstem Punkt\n"
      "[2]: 2opt Swap\n"
      "[3]: GA")

"""Algorithm Choice"""
algo = int(input())

# Greedy
if algo == 1:
    print("Führe aus: Greedy")
    greedy_route = greedy_algo(scatter_coordiantes, True)
    Gu.draw_node_based(img_ax, greedy_route)

    dist = 0.0
    for i, node in enumerate(greedy_route[:-1]):
        dist += distance(node, greedy_route[i + 1])
    print("Distanz: " + str(round(dist, 2)))
    show()

# 2-opt-Swap
elif algo == 2:
    print("Führe aus: 2opt Swap")
    random_route = random_route(scatter_coordiantes[:])  # Random Route
    fitness = distance_full(random_route)
    print("Start fitness " + str(fitness))

    best_route = random_route
    distance_best = distance_full(best_route)
    improve = True

    while improve:
        improve = False
        for i in range(1, len(random_route)-1):
            for j in range(i+1, len(random_route)):
                if j - i == 1:
                    continue
                new_route = two_opt_swap(copy.deepcopy(best_route), i, j)
                if distance_full(new_route) < distance_best:
                    best_route = new_route
                    distance_best = distance_full(new_route)
                    improve = True

                    img_ax.clear()
                    plt.axis("off")
                    img_ax.imshow(img)
                    Gu.draw_node_based(img_ax, best_route)
                    show(block=False)
                    plt.pause(0.01)
    print("End fitness " + str(distance_best))
    img_ax.clear()
    plt.imshow(img)
    plt.axis("off")
    Gu.scatter_plot_map(scatter_coordiantes, fig.add_subplot(111))
    Gu.draw_node_based(img_ax, best_route)
    show()

# GA
elif algo == 3:
    mutation_rate = 0.07  # Default: 0.07
    generation_size = 500  # Default: 500   | about 10 * (n_dimensions off Problem)
    min_generations = 1000  # Default: 1000 | Minimum >= lock_in_period
    lock_in_period = 500  # Default: 1000

    generation = 0
    pop = []
    pop_fit = []
    best = []
    track_best = []
    track_pop = []
    while True:
        """Initialize Population"""
        if generation == 0:
            pop.extend(genetic_algo_random_population(scatter_coordiantes, generation_size))
        generation += 1

        """Selection"""
        pop_fit = round(average_fitness(pop), 2)
        c_pop = pop[:]  # Cut all Individuals under Population average
        for i in c_pop:
            if distance_full(i) > pop_fit and len(pop) > 4:
                pop.remove(i)

        """Crossover"""
        e_pop = pop[:]  # Elite Population Group
        while len(pop) < generation_size:
            choice1 = random.choice(e_pop)
            choice2 = random.choice(e_pop)

            while choice1 == choice2:  # No crossover with self
                choice2 = random.choice(e_pop)

            offspring = genetic_algo_crossover(random.choice(e_pop), random.choice(e_pop))
            if offspring not in pop and offspring not in e_pop:  # Append Offspring to population if route doesnt allready exist
                pop.append(offspring)
        pop_fit = int(average_fitness(pop))

        """Mutation"""
        m_pop = [x for x in pop if x not in e_pop]  # Only Mutate offspring
        for i, route in enumerate(m_pop):
            while random.uniform(0, 1) < mutation_rate:
                i1 = random.randrange(0, len(route) - 1)
                i2 = random.randrange(0, len(route) - 1)

                while i1 == i2:  # No swap with self
                    i2 = random.randrange(0, len(route) - 1)
                pop[i] = swap(route, i1, i2)

        """Select Best Individual"""
        best_dist = int(distance_full(pop[0]))
        for k in pop:
            if distance_full(k) < best_dist:
                best = k
                best_dist = int(distance_full(k))

        track_best.append(best_dist)
        track_pop.append(pop_fit)

        # """Show generations best - very slow"""
        # img_ax.clear()
        # plt.axis("off")
        # img_ax.imshow(img)
        # Gu.draw_node_based(img_ax, best)
        # show(block=False)
        # plt.pause(0.01)

        """Status and Termination"""
        """Print Status every 100 generations, Check if minimum Generations reached,
        Check if current best fitness is at least 0.05% better then average of last 400"""
        if generation % 100 == 0:
            print("Generation: " + str(generation) + " | Population Fitness: " + str(
                pop_fit) + " | Best Individual: " + str(best_dist))
            if len(track_best) > min_generations and best_dist * 1.0005 > sum(track_best[-lock_in_period:])/lock_in_period:
                break

    """Show final"""
    best = pop[0]
    img_ax.clear()
    plt.imshow(img)
    plt.axis("off")
    Gu.scatter_plot_map(scatter_coordiantes, fig.add_subplot(111))
    Gu.draw_node_based(img_ax, best)
    show(block=False)
    plt.pause(0.01)

    """Show fitness  graph"""
    plt.figure(1)
    plt.suptitle("Fitness of best individuum")
    plt.ylabel('Fitness  as Total Route Distance (lower == better)')
    plt.xlabel('Generation')
    plt.plot(track_pop, label="Population average fitness ")
    plt.plot(track_best, label="Individual best fitness ")
    plt.legend(loc="upper right")
    plt.show()

else:
    print("Falsche Eingabe")
    input()

