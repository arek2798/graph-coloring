import random
from graphs_read import read_graph, find_num_of_nodes
from selection import select, roulette_wheel_selection, rank_selection_type, tournament_selection_type
from crossover import crossover, one_point_crossover_type, two_point_crossover_type
from mutation import mutate
from console_progressbar import ProgressBar

# Graph loading
graph = read_graph(".\\Graphs\\myciel6.col")

# Params:
POPULATION_SIZE = 200
CHROMOSOME_SIZE = find_num_of_nodes(graph)
GENES = range(1, CHROMOSOME_SIZE)
NUM_GENERATIONS = 100000
NUM_PARENTS_MATING = 40
MUTATION_PERCENT = 10

pb = ProgressBar(total=NUM_GENERATIONS, prefix='', suffix='', decimals=3, length=50, fill='*', zfill='-')

def initialize_population():
    population = list()

    for _ in range(POPULATION_SIZE):
        chromosome = list()
        for _ in range(CHROMOSOME_SIZE):
            chromosome.append(random.choice(GENES))
        population.append(chromosome)

    return population


def calculate_fitness(solution):
    conflicts = count_greedy_conflicts(solution, graph)
    color_usage = len(set(solution))
    heuristic_bonus = calculate_heuristic_bonus(solution, graph)

    alpha = 300  # conflicts
    beta = 1  # used_colors
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


# MAIN
initial_population = initialize_population()
population = []
generation = 0

for _ in range(len(initial_population)):
    population.append(calculate_fitness(initial_population[_]))

while generation < NUM_GENERATIONS:
    selected = select(population, NUM_PARENTS_MATING, tournament_selection_type)

    offspring = crossover(selected, CHROMOSOME_SIZE, two_point_crossover_type)

    mutated = mutate(offspring, MUTATION_PERCENT, GENES)

    new_population = []
    for child in mutated:
        new_population.append(calculate_fitness(child))

    population = new_population + population[:POPULATION_SIZE-len(new_population)]
    population = sorted(population, key=lambda x: -x[1])

    colors = len(list(set(population[0][0])))
    if colors == 1:
        break

    generation += 1
    pb.print_progress_bar(generation)


print("\nColors: {colors}".format(colors=len(list(set(population[0][0])))))
print("Solution: {colors}".format(colors=population[0][0]))

conflicts = count_greedy_conflicts(population[0][0], graph)
print("conflicts: {conflicts}".format(conflicts=conflicts))