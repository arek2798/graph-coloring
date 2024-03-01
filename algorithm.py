import random
from graphs_read import read_graph, find_num_of_nodes
from selection import select
from crossover import crossover
from mutation import mutate

# Graph loading
graph = read_graph(".\\Graphs\\myciel6.col")

# Params:
POPULATION_SIZE = 200
CHROMOSOME_SIZE = find_num_of_nodes(graph)
GENES = range(1, CHROMOSOME_SIZE)
NUM_GENERATIONS = 10000
NUM_PARENTS_MATING = 40
MUTATION_PERCENT = 10


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
generation = 1

for _ in range(len(initial_population)):
    population.append(calculate_fitness(initial_population[_]))

while generation <= NUM_GENERATIONS:
    # print("population size: {selected}".format(
    #     selected=len(population)))
    selected = select(population, NUM_PARENTS_MATING)

    offspring = crossover(selected, CHROMOSOME_SIZE)
    # print("offspring: {offspring}".format(offspring=len(offspring)))

    mutated = mutate(offspring, MUTATION_PERCENT, GENES)
    # print("mutated: {selected}".format(selected=len(mutated)))

    new_population = []
    for child in mutated:
        new_population.append(calculate_fitness(child))

    # print("new_population: {selected}".format(selected=len(new_population)))
    # print("new_population: {selected}".format(selected=new_population))
    # print("POPULATION_SIZE-len(new_population): {selected}".format(selected=POPULATION_SIZE-len(new_population)))
    # print("POPULATION_SIZE-len(new_population): {selected}".format(selected=population[0:(POPULATION_SIZE-len(new_population))]))
    # print("population size: {selected}".format(
    #     selected=len(population)))
    population = new_population + population[:POPULATION_SIZE-len(new_population)]
    # print("population: {selected}".format(selected=population))
    population = sorted(population, key=lambda x: -x[1])

    # print("Population: {population}".format(population=population))
    # print("Selected: {selected}".format(selected=selected))
    # print("Size: {size}".format(size=len(population)))
    colors = len(list(set(population[0][0])))
    if colors == 1:
        break

    print("Colors: {colors}".format(colors=colors))
    # print("Population: {colors}".format(colors=population))
    generation += 1
    print(generation)


print("Colors: {colors}".format(colors=len(list(set(population[0][0])))))
print("Solution: {colors}".format(colors=population[0][0]))
