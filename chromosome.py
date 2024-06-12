import random
import copy


class Chromosome:
    def __init__(self, graph, size=None, genes=None, solution=None):
        if solution is None:
            solution = {}

            for vertex in range(size):
                solution[vertex + 1] = random.choice(genes)

        self.graph = graph
        self.chromosome = solution
        self.fitness = self.calculate_fitness()
        self.conflicts = self.count_conflicts()

    def __len__(self):
        return len(self.chromosome)

    def get_chromosome(self):
        return self.chromosome

    def get_graph(self):
        return self.graph

    def get_num_of_colors(self):
        return len(set(list(self.chromosome.values())))

    def calculate_fitness(self):
        conflicts = self.count_conflicts()

        return 1 / (conflicts + 1)

    def count_conflicts(self):
        conflicts = 0
        for node in self.graph:

            color = self.chromosome[node]
            for neighbor in self.graph[node]:
                if self.chromosome.get(neighbor) == color:
                    conflicts += 1

        return conflicts

    def reduce_colors(self, genes):
        reduced_child = {}
        colors = list(set(list(self.chromosome.values())))

        for vertex in self.chromosome:
            index = colors.index(self.chromosome[vertex])
            if index >= len(genes):
                index = random.choice(genes)
            reduced_child[vertex] = index

        self.chromosome = reduced_child

        self.fitness = self.calculate_fitness()
        self.conflicts = self.count_conflicts()

    def mutate(self, genes, mutation_percent):
        mutated_chromosome = copy.deepcopy(self.chromosome)
        if random.random() < mutation_percent / 100:
            for gene in range(len(self.chromosome)):
                if random.random() < 1 / 100:
                    mutated_chromosome[gene+1] = random.choice(genes)

        else:
            for node in self.graph:
                color = mutated_chromosome[node]
                for neighbor in self.graph[node]:
                    if mutated_chromosome.get(neighbor) == color:
                        # new_color = random.choice(genes)
                        new_color = mutated_chromosome.get(neighbor) - 1
                        if new_color < 0:
                            new_color = len(genes) - 1
                        mutated_chromosome[neighbor] = new_color

        self.chromosome = mutated_chromosome

        self.fitness = self.calculate_fitness()
        self.conflicts = self.count_conflicts()
