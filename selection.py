from random import uniform, randint

roulette_wheel_selection_type = "ROULETTE_WHEEL_SELECTION"
rank_selection_type = "RANK_SELECTION"
tournament_selection_type = "TOURNAMENT_SELECTION"


def select(population, target, selection_type):
    if target >= len(population):
        return population

    selected_chromosomes = []

    population_copy = population.copy()

    for _ in range(target):
        if selection_type == roulette_wheel_selection:
            selected, index = roulette_wheel_selection(population_copy)
        elif selection_type == tournament_selection_type:
            selected, index = tournament_selection(population_copy)
        else:
            selected, index = rank_selection(population_copy)

        selected_chromosomes.append(selected)

        del population_copy[index]

    return selected_chromosomes


def roulette_wheel_selection(population):
    total_fitness = sum(chromosome[1] for chromosome in population)
    probabilities = [round(chromosome[1]/total_fitness, 10) for chromosome in population]

    cumulative_probability = [probabilities[0]]
    for probability in probabilities[1:]:
        cumulative_probability.append(round(probability+cumulative_probability[-1], 10))

    drawn_number = round(uniform(0, 1), 10)
    for rank, probability in enumerate(cumulative_probability):
        if drawn_number <= probability:
            return population[rank], rank

    return population[-1], len(population)-1


def tournament_selection(population):
    first = randint(0, len(population)-1)
    second = randint(0, len(population)-1)

    while second == first:
        second = randint(0, len(population) - 1)

    if population[first][1] > population[second][1]:
        return population[first], first

    return population[second], second


def rank_selection(population):
    population = sorted(population, key=lambda x: x[1])
    probabilities = calculate_probabilities(population)

    cumulative_probability = [probabilities[0]]
    for probability in probabilities[1:]:
        cumulative_probability.append(round(probability+cumulative_probability[-1], 10))

    drawn_number = round(uniform(0, 1), 10)
    for rank, probability in enumerate(cumulative_probability):
        if drawn_number <= probability:
            return population[rank], rank

    return population[-1], len(population) - 1


def calculate_probabilities(population):
    probabilities = []

    probability_per_rank = calculate_probability_per_rank(population)

    for rank, chromosome in enumerate(population):
        probabilities.append(round((rank + 1) * probability_per_rank, 10))

    return probabilities


def calculate_probability_per_rank(population):
    rank_sum = 0

    for rank, _ in enumerate(population):
        rank_sum += rank + 1

    return 100/rank_sum
