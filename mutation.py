import random

def mutate(offspring, percent, genes):
    mutated_offspring = []

    for child in offspring:
        for gene in range(len(child)):
            if random.random() < percent/100:
                child[gene] = random.choice(genes)

        mutated_offspring.append(child)

    return mutated_offspring
