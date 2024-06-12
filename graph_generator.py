import networkx as nx
import random


def generate_graph(num_vertices, density):
    graph = nx.Graph()

    # Dodawanie wierzchołków
    graph.add_nodes_from(range(1, num_vertices + 1))
    edges = 0

    # Dodawanie krawędzi zgodnie z określoną gęstością
    for i in range(1, num_vertices + 1):
        for j in range(i + 1, num_vertices + 1):
            edges += 1
            if random.random() < density:
                graph.add_edge(i, j)

    # Liczba krawędzi może się różnić od oczekiwanej gęstości ze względu na losowość
    num_edges = graph.number_of_edges()

    with open(f"graphs/generated/graph_generated_{num_vertices}_{num_edges}_{density}.col", "w") as file:
        file.write(f"p edge {num_vertices} {num_edges}\n")

        for edge in graph.edges():
            file.write(f"e {edge[0]} {edge[1]}\n")

    print("Graph generated")
