from chromosome import Chromosome
from selection import roulette_wheel_selection, tournament_selection, rank_selection, rank_selection_type, roulette_wheel_selection_type
import copy


class Population:
    def __init__(self, population_size=None, chromosome_size=None, genes=None, graph=None, chromosomes=None, selection_type=None):
        population = []
        if chromosomes is None:
            for _ in range(population_size):
                chromosome = Chromosome(graph, chromosome_size, genes)
                population.append(chromosome)
        else:
            population = chromosomes

        self.population = population

        if selection_type == roulette_wheel_selection_type:
            self.selection_method = roulette_wheel_selection
        elif selection_type == rank_selection_type:
            self.selection_method = rank_selection
        else:
            self.selection_method = tournament_selection

    def __len__(self):
        return len(self.population)

    def reduce_colors(self, genes):
        for chromosome in self.population:
            chromosome.reduce_colors(genes)

    def select(self, percent):
        if percent >= 100:
            return self.population

        target = int(percent/100 * len(self.population))

        selected_chromosomes = []

        for _ in range(target):
            chromosome = self.selection_method(self.population)
            selected_chromosomes.append(copy.deepcopy(chromosome))

        return selected_chromosomes

    def get_best_chromosomes(self, num_of):
        sorted_population = sorted(self.population, key=lambda chromosome: -chromosome.fitness)
        return sorted_population[:num_of]
