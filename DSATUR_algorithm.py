def dsatur(graph):
    # Inicjalizacja zmiennych
    n = len(graph)
    colors = {node: None for node in graph}
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    saturation = {node: 0 for node in graph}

    # Wybór pierwszego wierzchołka o najwyższym stopniu
    current_node = max(degrees, key=degrees.get)

    for _ in range(n):
        # Wybór koloru
        if colors[current_node] is None:
            neighbor_colors = get_neighbor_colors(graph, colors, current_node)
            for color in range(n):
                if color not in neighbor_colors:
                    colors[current_node] = color
                    break

        # Aktualizacja saturacji sąsiadów
        update_saturation_degrees(graph, colors, current_node, saturation)

        # Znajdowanie kolejnego wierzchołka do kolorowania
        uncolored_nodes = [node for node in graph if colors[node] is None]
        if not uncolored_nodes:
            break
        current_node = max(uncolored_nodes, key=lambda node: (saturation[node], degrees[node]))

    return colors


def update_saturation_degrees(graph, colors, node, saturation):
    for neighbor in graph[node]:
        if colors[neighbor] is None:
            unique_colors = set(colors[n] for n in graph[neighbor] if colors[n] is not None)
            saturation[neighbor] = len(unique_colors)


def get_neighbor_colors(graph, colors, node):
    return set(colors[neighbor] for neighbor in graph[node] if colors[neighbor] is not None)
