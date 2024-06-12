from random import uniform, randint

roulette_wheel_selection_type = "ROULETTE_WHEEL_SELECTION"
rank_selection_type = "RANK_SELECTION"
tournament_selection_type = "TOURNAMENT_SELECTION"


def roulette_wheel_selection(population):
    total_fitness = sum(chromosome.fitness for chromosome in population)
    probabilities = [round(chromosome.fitness / total_fitness, 10) for chromosome in population]

    cumulative_probability = [probabilities[0]]
    for probability in probabilities[1:]:
        cumulative_probability.append(round(probability + cumulative_probability[-1], 10))

    drawn_number = round(uniform(0, 1), 10)
    for rank, probability in enumerate(cumulative_probability):
        if drawn_number <= probability:
            return population[rank]

    return population[-1]


def tournament_selection(population):
    first = randint(0, len(population)-1)
    second = randint(0, len(population)-1)

    while second == first:
        second = randint(0, len(population) - 1)

    if population[first].fitness > population[second].fitness:
        return population[first]

    return population[second]


def rank_selection(population):
    population = sorted(population, key=lambda chromosome: chromosome.fitness)
    probabilities = calculate_probabilities(population)

    cumulative_probability = [probabilities[0]]
    for probability in probabilities[1:]:
        cumulative_probability.append(round(probability+cumulative_probability[-1], 10))

    drawn_number = round(uniform(0, 100), 10)
    for rank, probability in enumerate(cumulative_probability):
        if drawn_number <= probability:
            return population[rank]

    return population[-1]


def calculate_probabilities(population):
    probabilities = []

    probability_per_rank = calculate_probability_per_rank(population)

    for rank, _ in enumerate(population):
        probabilities.append(round((rank + 1) * probability_per_rank, 10))

    return probabilities


def calculate_probability_per_rank(population):
    rank_sum = 0

    for rank, _ in enumerate(population):
        rank_sum += rank + 1

    return 100/rank_sum
