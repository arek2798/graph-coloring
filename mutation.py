def mutate(offspring, genes, mutation_percent):
    mutated_offspring = []

    for child in offspring:
        child.mutate(genes, mutation_percent)

        mutated_offspring.append(child)

    return mutated_offspring
