import random
from init_generation import expand_adjacency_list


def mutate(offspring, percent, genes):
    mutated_offspring = []
    for child in offspring:
        for gene in range(len(child)):
            if random.random() < percent/100:
                child[gene] = random.choice(genes)

        mutated_offspring.append(child)

    return mutated_offspring


def mutate2(offspring, graph, genes, mutation_percent):
    mutated_offspring = []
    # extended_graph = expand_adjacency_list(graph, len(offspring[0])) #remove

    for child in offspring:
        if random.random() < mutation_percent / 100:
            for gene in range(len(child)):
                if random.random() < 4 / 100:
                    child[gene] = random.choice(genes)

            mutated_offspring.append(child)
            continue

        for node in graph:
            color = child[node]
            for neighbor in graph[node]:
                if child.get(neighbor) == color:
                    # new_color = random.choice(genes)
                    new_color = child[neighbor]-1
                    if new_color < 0:
                        new_color = len(genes)-1
                    child[neighbor] = new_color

        mutated_offspring.append(child)

    return mutated_offspring


def mutate3(offspring, graph, genes, mutation_percent):
    mutated_offspring = []

    for child in offspring:
        if random.random() < (mutation_percent / 100):
            # if random.random() < 40 / 100:
            #     vertex = random.randint(1, len(child))
            # else:
            vertex = get_vertex_with_most_conflicts(child, graph)

            child[vertex] = random.choice(genes)
            # new_child = child
            # new_child[vertex] = random.choice(genes)
            # old_fitness = calculate_fitness(child, graph)
            # new_fitness = calculate_fitness(new_child, graph)
            # print("old_fitness:", old_fitness[1], "new_fitness:", new_fitness[1])
            # print("old_child:", child)
            # print("new_child:", new_child)
            # if new_fitness[1] > old_fitness[1]:
            #     print("better")
            #     child = new_child

            # continue

        mutated_offspring.append(child)

    return mutated_offspring


def get_vertex_with_most_conflicts(solution, graph):
    extended_graph = expand_adjacency_list(graph, len(solution))
    conflicts_per_vertex = {i: 0 for i in range(1, len(extended_graph)+1)}

    for node in extended_graph:
        color = solution[node]
        for neighbor in extended_graph[node]:
            if solution.get(neighbor) == color:
                conflicts_per_vertex[node] += 1

    vertex = max(conflicts_per_vertex, key=conflicts_per_vertex.get)
    # print(vertex)
    # print(conflicts_per_vertex)

    return vertex


def calculate_fitness(solution, graph):
    conflicts = count_greedy_conflicts(solution, graph)
    # color_usage = len(set(list(solution.values())))
    # heuristic_bonus = calculate_heuristic_bonus(solution, graph)

    alpha = 4  # conflicts
    beta = 2  # used_colors
    gamma = 0.8  # bonus

    # fitness = 1 / (alpha * (conflicts + 1) + beta * (color_usage + 1) + gamma * heuristic_bonus)
    # fitness = 1 / (alpha * (conflicts + 1) + beta * (color_usage + 1))

    # return [solution, fitness]
    return [solution, 1/(conflicts+1)]


def count_greedy_conflicts(solution, graph):
    conflicts = 0
    for node in graph:

        color = solution[node]
        for neighbor in graph[node]:
            if solution.get(neighbor) == color:
                conflicts += 1

    return conflicts