import random
from chromosome import Chromosome

one_point_crossover_type = "ONE_POINT_CROSSOVER"
two_point_crossover_type = "TWO_POINT_CROSSOVER"


def crossover(chromosomes):
    chromosomes = sorted(chromosomes, key=lambda chromosome: -chromosome.fitness)

    offspring = []

    for i in range(int(len(chromosomes)/2)):
        parent1 = chromosomes[2*i]
        parent2 = chromosomes[2*i+1]

        # children = one_point_crossover(parent1, parent2)
        children = two_point_crossover(parent1, parent2)

        offspring.extend(children)

    return offspring


def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1)-1)
    child1 = {}
    child2 = {}
    for vertex in range(len(parent1)):
        if vertex < crossover_point:
            child1[vertex+1] = parent1.get_chromosome().get(vertex + 1)
            child2[vertex+1] = parent2.get_chromosome().get(vertex + 1)
        else:
            child1[vertex+1] = parent2.get_chromosome().get(vertex + 1)
            child2[vertex+1] = parent1.get_chromosome().get(vertex + 1)

    return [Chromosome(parent1.get_graph(), solution=child1), Chromosome(parent1.get_graph(), solution=child2)]


def two_point_crossover(parent1, parent2):
    point1 = random.randint(1, len(parent1) - 1)
    point2 = random.randint(1, len(parent1) - 1)

    while point1 == point2:
        point2 = random.randint(1, len(parent1) - 1)

    if point1 > point1:
        buf = point1
        point1 = point2
        point2 = buf

    child1 = {}
    child2 = {}
    for vertex in range(len(parent1)):
        if point1 < vertex < point2:
            child1[vertex + 1] = parent1.get_chromosome().get(vertex + 1)
            child2[vertex + 1] = parent2.get_chromosome().get(vertex + 1)
        else:
            child1[vertex + 1] = parent2.get_chromosome().get(vertex + 1)
            child2[vertex + 1] = parent1.get_chromosome().get(vertex + 1)

    return [Chromosome(parent1.get_graph(), solution=child1), Chromosome(parent1.get_graph(), solution=child2)]
