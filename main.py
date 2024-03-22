import random
import os
from graphs_read import read_graph, find_num_of_nodes, plot_graph
from selection import select, roulette_wheel_selection_type, rank_selection_type, tournament_selection_type
from crossover import crossover, one_point_crossover_type, two_point_crossover_type
from mutation import mutate
from console_progressbar import ProgressBar


def initialize_population(population_size, chromosome_size, genes):
    init_population = list()

    for _ in range(population_size):
        chromosome = list()
        for _ in range(chromosome_size):
            chromosome.append(random.choice(genes))
        init_population.append(chromosome)

    return init_population


def calculate_fitness(solution, graph):
    conflicts = count_greedy_conflicts(solution, graph)
    color_usage = len(set(solution))
    heuristic_bonus = calculate_heuristic_bonus(solution, graph)

    alpha = 15  # conflicts
    beta = 2  # used_colors
    gamma = 0.8  # bonus

    fitness = 1 / (alpha * (conflicts + 1) + beta * (color_usage + 1) + gamma * heuristic_bonus)

    return [solution, fitness]


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


def main():
    graphs = os.listdir(".\\Graphs\\")

    plots = []
    for graphFile in graphs:
        print("\nGraph: {graphName}".format(graphName=graphFile))

        # Graph loading
        graph = read_graph(f".\\Graphs\\{graphFile}")

        # Params:
        population_size = 200
        chromosome_size = find_num_of_nodes(graph)
        genes = range(1, chromosome_size)
        num_generations = 50000
        num_parents_mating = 80
        mutation_percent = 10

        pb = ProgressBar(total=num_generations, prefix='', suffix='', decimals=3, length=50, fill='*', zfill='-')

        initial_population = initialize_population(population_size, chromosome_size, genes)
        population = []
        generation = 0
        best_colors_per_population = []

        for _ in range(len(initial_population)):
            population.append(calculate_fitness(initial_population[_], graph))

        while generation < num_generations:
            selected = select(population, num_parents_mating, roulette_wheel_selection_type)

            offspring = crossover(selected, chromosome_size, one_point_crossover_type)

            mutated = mutate(offspring, mutation_percent, genes)

            new_population = []
            for child in mutated:
                new_population.append(calculate_fitness(child, graph))

            population = new_population + population[:population_size-len(new_population)]
            population = sorted(population, key=lambda x: -x[1])

            colors = len(list(set(population[0][0])))
            best_colors_per_population.append(colors)
            if colors == 1:
                break

            generation += 1
            pb.print_progress_bar(generation)

        print("\nColors: {colors}".format(colors=len(list(set(population[0][0])))))
        print("Best solution: {solution}".format(solution=population[0][0]))

        conflicts = count_greedy_conflicts(population[0][0], graph)
        print("Color conflicts: {conflicts}".format(conflicts=conflicts))

        plots.append([graphFile, best_colors_per_population])

        # plot_graph(best_colors_per_population, label_x="Generacja", label_y="Liczba kolorów", title="Najmniejsza liczba kolorów w stosunku do generacji")

    for graph in plots:
        print(graph[0])
        plot_graph(graph[1], label_x="Generacja", label_y="Liczba kolorów",
               title="Najmniejsza liczba kolorów w stosunku do generacji")


if __name__ == '__main__':
    main()
