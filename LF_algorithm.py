import os
import time
import pandas as pd
from datetime import datetime
from graph_reader import read_graph
from utils import expand_adjacency_list, count_greedy_conflicts, find_num_of_nodes
from prettytable import PrettyTable
from DSATUR_algorithm import dsatur


def largest_first_coloring(graph):
    # Sortowanie wierzchołków według ich stopnia w kolejności malejącej
    vertices_sorted = sorted(graph, key=lambda v: len(graph[v]), reverse=True)

    vertex_color = {}

    for vertex in vertices_sorted:
        # Znalezienie dostępnych kolorów, sprawdzając kolory sąsiadów
        neighbor_colors = {vertex_color.get(neighbor) for neighbor in graph[vertex] if neighbor in vertex_color}

        color = 0
        while color in neighbor_colors:
            color += 1

        vertex_color[vertex] = color

    return vertex_color


def main():
    graphs = os.listdir(".\\Graphs\\Generated\\")

    plots = []

    for graph_file in graphs:
        print("\nGraph: {graphName}".format(graphName=graph_file))

        graph = read_graph(f".\\Graphs\\Generated\\{graph_file}")
        chromosome_size = find_num_of_nodes(graph)

        extended_graph = expand_adjacency_list(graph, chromosome_size)

        start_time = datetime.now()

        # LF
        # vertex_color = largest_first_coloring(extended_graph)
        # DSATUR
        vertex_color = dsatur(extended_graph)

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
