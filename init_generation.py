def initialize_weights(V):
    return {v: 1 for v in V}


def calculate_surrogate_constraint(V, adj, weights):
    surrogate = {}
    for v in V:
        surrogate[v] = sum(weights[u] for u in adj[v] if u in weights)
    return surrogate


def select_vertex(surrogate):
    return min(surrogate, key=surrogate.get)


def update_weights(vertex, adj, weights):
    for neighbor in adj[vertex]:
        if neighbor in weights:
            weights[neighbor] = 0
    return weights


def expand_adjacency_list(adjacency_list, num_vertices):
    full_graph = {k: [] for k in range(1, num_vertices+1)}

    for vertex in adjacency_list:
        for neighbor in adjacency_list[vertex]:
            full_graph[vertex].append(neighbor)

            if vertex not in full_graph[neighbor]:
                full_graph[neighbor].append(vertex)

    return full_graph


def DBG_algorithm(num_vertices, adjacency_list):
    independent_sets = []
    remaining_vertices = list(range(1, num_vertices+1))

    adjacency_list = expand_adjacency_list(adjacency_list, num_vertices)

    while remaining_vertices:
        current_set = []
        weights = initialize_weights(remaining_vertices)

        while remaining_vertices and any(weight > 0 for weight in weights.values()):
            surrogate = calculate_surrogate_constraint(remaining_vertices, adjacency_list, weights)
            selected_vertex = select_vertex(surrogate)
            current_set.append(selected_vertex)
            remaining_vertices.remove(selected_vertex)
            weights = update_weights(selected_vertex, adjacency_list, weights)
            weights[selected_vertex] = 0
            weights = {v: w for v, w in weights.items() if w > 0}
        independent_sets.append(current_set)

    return independent_sets
