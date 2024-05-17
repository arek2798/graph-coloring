def sorted_largest_first_coloring(graph):
    # Inicjalizacja słownika, który przypisze wierzchołkom kolory
    vertex_color = {}
    # Inicjalizacja zbioru niepokolorowanych wierzchołków
    uncolored_vertices = set(graph.keys())
    # Inicjalizacja kolejki priorytetowej, której elementy to krotki (liczba pokolorowanych sąsiadów, stopień, wierzchołek)
    priority_queue = [(-len(graph[v]), v) for v in graph]
    # Sortowanie początkowe według stopnia wierzchołka (największy na początku)
    priority_queue.sort()

    # Pętla działa, dopóki są niepokolorowane wierzchołki
    while priority_queue:
        # Wybieramy wierzchołek o największym stopniu z maksymalną liczbą pokolorowanych sąsiadów
        _, vertex = priority_queue.pop(0)
        if vertex in uncolored_vertices:
            # Znalezienie dostępnych kolorów, sprawdzając kolory sąsiadów
            neighbor_colors = {vertex_color.get(neighbor) for neighbor in graph[vertex] if neighbor in vertex_color}

            # Znalezienie najmniejszego dostępnego koloru
            color = 0
            while color in neighbor_colors:
                color += 1

            # Przypisanie koloru do wierzchołka
            vertex_color[vertex] = color
            # Usunięcie wierzchołka z niepokolorowanych
            uncolored_vertices.remove(vertex)

            # Aktualizacja kolejki z nowymi wartościami liczby pokolorowanych sąsiadów
            priority_queue = [(-sum(1 for neighbor in graph[v] if neighbor not in uncolored_vertices), v)
                              for v in uncolored_vertices]
            priority_queue.sort()

    return vertex_color
