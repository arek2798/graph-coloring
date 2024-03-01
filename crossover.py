import random


def crossover(chromosomes, chromosome_size):
    chromosomes = sorted(chromosomes, key=lambda x: -x[1])

    offspring = []

    for i in range(int(len(chromosomes)/2)):
        parent1 = chromosomes[2*i][0]
        parent2 = chromosomes[2*i+1][0]

        crossover_point = random.randint(1, chromosome_size-1)
        child = parent1[:crossover_point] + parent2[crossover_point:]

        offspring.extend([child])

    return offspring
