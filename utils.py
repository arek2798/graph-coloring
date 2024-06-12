import numpy as np


def count_greedy_conflicts(solution, graph):
    conflicts = 0
    for node in graph:

        color = solution[node]
        for neighbor in graph[node]:
            if solution.get(neighbor) == color:
                conflicts += 1

    return conflicts


def expand_adjacency_list(adjacency_list, num_vertices):
    full_graph = {k: [] for k in range(1, num_vertices+1)}

    for vertex in adjacency_list:
        for neighbor in adjacency_list[vertex]:
            full_graph[vertex].append(neighbor)

            if vertex not in full_graph[neighbor]:
                full_graph[neighbor].append(vertex)

    return full_graph


def find_num_of_nodes(dictionary):
    max_value = 0
    for key in dictionary:
        if np.max(dictionary[key]) > max_value:
            max_value = np.max(dictionary[key])

    return max_value
