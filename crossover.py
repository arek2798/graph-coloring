import random


one_point_crossover_type = "ONE_POINT_CROSSOVER"
two_point_crossover_type = "TWO_POINT_CROSSOVER"


def crossover(chromosomes, chromosome_size, crossover_type):
    chromosomes = sorted(chromosomes, key=lambda x: -x[1])

    offspring = []

    for i in range(int(len(chromosomes)/2)):
        parent1 = chromosomes[2*i][0]
        parent2 = chromosomes[2*i+1][0]

        childs = one_point_crossover(parent1, parent2, chromosome_size)
        # child = two_point_crossover(parent1, parent2, chromosome_size)
        # print(child)
        # if crossover_type == one_point_crossover_type:
        #     child = one_point_crossover(parent1, parent2, chromosome_size)
        # else:
        #     child = two_point_crossover(parent1, parent2, chromosome_size)

        offspring.extend(childs)

    return offspring


def one_point_crossover(parent1, parent2, chromosome_size):
    crossover_point = random.randint(1, chromosome_size)
    # child = parent1[:crossover_point] + parent2[crossover_point:]
    # child = list(parent1.items())[:crossover_point] + list(parent2.items())[crossover_point:]
    child1 = {}
    child2 = {}
    for vertex in range(chromosome_size):
        if vertex < crossover_point:
            child1[vertex+1] = parent1.get(vertex+1)
            child2[vertex+1] = parent2.get(vertex+1)
        else:
            child1[vertex+1] = parent2.get(vertex+1)
            child2[vertex+1] = parent1.get(vertex + 1)

    return [child1, child2]


def two_point_crossover(parent1, parent2, chromosome_size):
    crossover_point = random.randint(1, chromosome_size - 1)
    second_crossover_point = random.randint(1, chromosome_size - 1)

    while crossover_point == second_crossover_point:
        second_crossover_point = random.randint(1, chromosome_size - 1)

    if crossover_point < second_crossover_point:
        child = parent1[:crossover_point] + parent2[crossover_point:second_crossover_point] + parent1[second_crossover_point:]
    else:
        child = parent1[:second_crossover_point] + parent2[second_crossover_point:crossover_point] + parent1[crossover_point:]

    return child