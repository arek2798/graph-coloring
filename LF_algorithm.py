import os
import time
import pandas as pd
from datetime import datetime
from graphs_read import read_graph, find_num_of_nodes, plot_graph
from init_generation import expand_adjacency_list
from prettytable import PrettyTable
from main import count_greedy_conflicts
from SLF_algorithm import sorted_largest_first_coloring


def largest_first_coloring(graph):
    # Sortowanie wierzchołków według ich stopnia w kolejności malejącej
    vertices_sorted = sorted(graph, key=lambda v: len(graph[v]), reverse=True)

    # Słownik do przechowywania kolorów przypisanych do wierzchołków
    vertex_color = {}

    # Przechodzenie przez posortowaną listę wierzchołków
    for vertex in vertices_sorted:
        # Znalezienie dostępnych kolorów, sprawdzając kolory sąsiadów
        neighbor_colors = {vertex_color.get(neighbor) for neighbor in graph[vertex] if neighbor in vertex_color}

        # Znalezienie najmniejszego koloru, który nie jest używany przez sąsiadów
        color = 0
        while color in neighbor_colors:
            color += 1

        # Przypisanie koloru do wierzchołka
        vertex_color[vertex] = color

    return vertex_color


def main():
    # graphs = os.listdir(".\\Graphs\\Generated\\")
    graphs = {
    #     "fpsol2.i.1.col": 65,
    #     "zeroin.i.1.col": 49,
    #     "latin_square_10.col": 49,
        "le450_15a.col": 15,
    }
    plots = []
    print("start")
    for graph_file in graphs:
        print("\nGraph: {graphName}".format(graphName=graph_file))

        # graph = read_graph(f".\\Graphs\\Generated\\{graph_file}")
        graph = read_graph(f".\\Graphs\\{graph_file}")
        chromosome_size = find_num_of_nodes(graph)

        extended_graph = expand_adjacency_list(graph, chromosome_size)

        start_time = datetime.now()

        # vertex_color = largest_first_coloring(extended_graph)
        vertex_color = sorted_largest_first_coloring(extended_graph)

        end_time = datetime.now()

        colors = len(set(list(vertex_color.values())))
        print("\nColors: {colors}".format(colors=colors))
        print("Solution: {solution}".format(solution=vertex_color))

        conflicts = count_greedy_conflicts(vertex_color, graph)
        print("Color conflicts: {conflicts}".format(conflicts=conflicts))

        exec_time = end_time - start_time
        print("Time: {time}".format(time=exec_time))

        plots.append([graph_file, colors, conflicts, str(exec_time)])

    # Save results
    table = PrettyTable()
    table.field_names = ["Graph name", "Colors", "Conflicts", "Time"]

    excel_rows = []

    for graph in plots:
        table.add_row([f"{graph[0]}", graph[1], graph[2], graph[3]])
        excel_rows.append([f"{graph[0]}", graph[1], graph[2], graph[3]])

    df = pd.DataFrame(excel_rows, columns=["Graph name", "Colors", "Conflicts", "Time"])
    df.to_excel(f".\\plots\\Generated\\result_{time.time()}.xlsx", index=False)
    print(table)


if __name__ == '__main__':
    main()
