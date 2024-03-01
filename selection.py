from random import uniform


def select(population, target):
    if target >= len(population):
        return population

    selected_chromosomes = []

    population_copy = population.copy()

    for _ in range(target):
        selected, index = roulette_wheel_selection(population_copy)
        # print("selected: {selected}".format(selected=selected))
        selected_chromosomes.append(selected)

        # population_copy.remove(selected)
        del population_copy[index]

    return selected_chromosomes


def roulette_wheel_selection(population):
    total_fitness = sum(chromosome[1] for chromosome in population)
    probabilities = [round(chromosome[1]/total_fitness, 10) for chromosome in population]

    cumulative_probability = [probabilities[0]]
    for probability in probabilities[1:]:
        cumulative_probability.append(round(probability+cumulative_probability[-1], 10))

    drawn_number = round(uniform(0, 1), 10)
    # print("drawn_number: {selected}".format(selected=drawn_number))
    # print("cumulative_probability: {selected}".format(selected=cumulative_probability))
    for index, probability in enumerate(cumulative_probability):
        if drawn_number <= probability:
            return population[index], index

    return population[-1], len(population)-1