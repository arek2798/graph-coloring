import pygad

from graphs_read import read_graph, plot_graph, find_max_from_dictionary

graph = read_graph(".\\Graphs\\queen6_6.col")
used_colors = {}
bad_edges = {}

# definiujemy parametry chromosomu
# geny to liczby: 0 lub 1
print(graph)
numOfGenes = int(find_max_from_dictionary(graph))
gene_space = range(1, numOfGenes)


def fitness_func(ga_instance, solution, solution_idx):
    print("generations_completed", ga_instance.generations_completed)

    # conflicts = count_greedy_conflicts(solution, graph)
    # if solution_idx in bad_edges:
    #     bad_edges[solution_idx].append(conflicts)
    # else:
    #     bad_edges[solution_idx] = [conflicts]
    #
    # color_usage = len(set(solution))
    # if solution_idx in used_colors:
    #     used_colors[solution_idx].append(color_usage)
    # else:
    #     used_colors[solution_idx] = [color_usage]
    #
    # return 1 / (1 + conflicts + color_usage)

    conflicts = count_greedy_conflicts(solution, graph)
    color_usage = len(set(solution))
    heuristic_bonus = calculate_heuristic_bonus(solution, graph)

    alpha = 1  # conflicts
    beta = 1  # used_colors
    gamma = 0.8  # bonus

    fitness = 1 / (alpha * (conflicts + 1) + beta * (color_usage + 1) + gamma * heuristic_bonus)

    return fitness


def count_greedy_conflicts(solution, graph):
    conflicts = 0
    for node in graph:
        color = solution[node - 1]
        for neighbor in graph[node]:
            if solution[neighbor - 1] == color:
                conflicts += 1
    return conflicts


def calculate_heuristic_bonus(solution, graph):
    bonus = 0
    for node in graph:
        unique_colors_in_neighborhood = len(set(solution[neighbor-1] for neighbor in graph[node]))
        bonus += 1 / (unique_colors_in_neighborhood + 1)
    return bonus


# ile chromsomów w populacji
# ile genow ma chromosom
sol_per_pop = 200
num_genes = numOfGenes

# ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
# ile pokolen
# ilu rodzicow zachowac (kilka procent)
num_parents_mating = 100
num_generations = 10000
keep_parents = 10

# jaki typ selekcji rodzicow?
# sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "rws"

# w il =u punktach robic krzyzowanie?
crossover_type = "two_points"

# mutacja ma dzialac na ilu procent genow?
# trzeba pamietac ile genow ma chromosom
mutation_type = "random"
mutation_percent_genes = 10

# inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
ga_instance = pygad.GA(gene_space=gene_space,
                       num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)

# uruchomienie algorytmu
ga_instance.run()

# podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Colors: {colors}".format(colors=len(list(set(solution)))))

# ga_instance.plot_fitness()
# plot_graph(used_colors[1], "wykorzystane kolory", "Generacja", "Liczba kolorów")
# plot_graph(bad_edges[1], "Konflikty", "Generacja", "Konflikty")
