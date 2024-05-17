import random
import os
import time
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
from graphs_read import read_graph, find_num_of_nodes, plot_graph
from selection import select, roulette_wheel_selection_type, rank_selection_type, tournament_selection_type
from crossover import crossover, one_point_crossover_type, two_point_crossover_type
from mutation import mutate, mutate2, mutate3
from init_generation import DBG_algorithm
from console_progressbar import ProgressBar
from prettytable import PrettyTable
from graphs_generate import generate_graph


def initialize_population2(population_size, adjacency_list, genes, chromosome_size):
    population = []

    for _ in range(population_size):
        coloring = {}
        independent_sets = DBG_algorithm(chromosome_size, adjacency_list)
        for color_index, independent_set in enumerate(independent_sets):
            for vertex in independent_set:
                if color_index >= len(genes):
                    coloring[vertex] = random.choice(genes)
                else:
                    coloring[vertex] = color_index
        population.append(coloring)

    return population


def initialize_population(population_size, chromosome_size, genes):
    init_population = []

    for _ in range(population_size):
        chromosome = {}
        for vertex in range(chromosome_size):
            chromosome[vertex+1] = random.choice(genes)
        init_population.append(chromosome)

    return init_population


def reduce_population_colors(population, genes):
    reduced_population = []

    for child in population:
        reduced_child = {}
        colors = list(set(list(child[0].values())))
        for vertex in child[0]:
            index = colors.index(child[0][vertex])
            if index >= len(genes):
                index = random.choice(genes)
            reduced_child[vertex] = index

        reduced_population.append(reduced_child)

    return reduced_population


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


def calculate_heuristic_bonus(solution, graph):
    bonus = 0
    for node in graph:
        unique_colors_in_neighborhood = len(set(solution.get(neighbor) for neighbor in graph.get(node)))
        bonus += unique_colors_in_neighborhood/len(graph.get(node))
        # bonus += 1 / (unique_colors_in_neighborhood + 1)
    return bonus

def count_child_size(population):
    sizes = {}

    for child in population:
        length = len(child[0])
        if length in sizes:
            sizes[length] += 1
        else:
            sizes[length] = 1

    # print(sizes)
    return sizes

def main():
    # for i in range(10):
    #     # generate_graph((i+1)*10, round((i+1)*0.05, 2))
    #     generate_graph(400, round((i + 1) * 0.02, 2))


    # graphs = os.listdir(".\\Graphs\\Generated\\")
    # graphs = []
    graphs = {
        # "fpsol2.i.1.col": 65,
        # "fpsol2.i.2.col": 30,
        # "fpsol2.i.3.col": 30,
        "le450_15a.col": 15,
        # "le450_15b.col": 15,
        # "le450_15c.col": 15,
        # "le450_15d.col": 15,
        # "le450_25a.col": 25,
        # "le450_25b.col": 25,
        # "le450_25c.col": 25,
        # "le450_25d.col": 25,
        # "miles250.col": 8,
        # "miles500.col": 20,
        # "miles750.col": 31,
        # "miles1000.col": 42,
        # "miles1500.col": 73,
        # "mulsol.i.1.col": 49,
        # "mulsol.i.2.col": 31,
        # "mulsol.i.3.col": 31,
        # "mulsol.i.4.col": 31,
        # "mulsol.i.5.col": 31,
        # "myciel3.col": 4,
        # "myciel4.col": 5,
        # "myciel5.col": 6,
        # "myciel6.col": 7,
        # "myciel7.col": 8,
        # "queen5_5.col": 5,
        # "queen6_6.col": 7,
        # "queen7_7.col": 7,
        # "queen8_8.col": 9,
        # "queen9_9.col": 10,
        # "zeroin.i.1.col": 49,
        # "zeroin.i.2.col": 30,
        # "zeroin.i.3.col": 30,

        # Generated
        # "graph_generated_200_388_0.02.col": 4,
        # "graph_generated_200_743_0.04.col": 6,
        # "graph_generated_200_1199_0.06.col": 7,
        # "graph_generated_200_1576_0.08.col": 8,
        # "graph_generated_200_2017_0.1.col": 10,
        # "graph_generated_200_2456_0.12.col": 11,
        # "graph_generated_200_2860_0.14.col": 12,
        # "graph_generated_200_3134_0.16.col": 13,
        # "graph_generated_200_3637_0.18.col": 15,
        # "graph_generated_200_3967_0.2.col": 16,
        # "graph_generated_300_917_0.02.col": 5,
        # "graph_generated_300_1871_0.04.col": 7,
        # "graph_generated_300_2589_0.06.col": 9,
        # "graph_generated_300_3639_0.08.col": 12,
        # "graph_generated_300_4410_0.1.col": 13,
        # "graph_generated_300_5321_0.12.col": 14,
        # "graph_generated_300_6221_0.14.col": 16,
        # "graph_generated_300_7252_0.16.col": 18,
        # "graph_generated_300_8167_0.18.col": 19,
        # "graph_generated_300_8955_0.2.col": 20,
        # "graph_generated_400_1585_0.02.col": 6,
        # "graph_generated_400_3071_0.04.col": 9,
        # "graph_generated_400_4815_0.06.col": 11,
        # "graph_generated_400_6288_0.08.col": 14,
        # "graph_generated_400_7877_0.1.col": 15,
        # "graph_generated_400_9518_0.12.col": 18,
        # "graph_generated_400_11130_0.14.col": 20,
        # "graph_generated_400_12734_0.16.col": 22,
        # "graph_generated_400_14416_0.18.col": 24,
        # "graph_generated_400_15933_0.2.col": 26,
    }
    plots = []
    selection_type = rank_selection_type
    crossover_type = one_point_crossover_type
    num_of_measurements = 1

    for graph_file in graphs:
        print("\nGraph: {graphName}".format(graphName=graph_file))

        for measure_num in range(num_of_measurements):
            print(f"\nMeasurement: {measure_num+1}/{num_of_measurements}")

            # Graph loading
            # graph = read_graph(f".\\Graphs\\Generated\\{graph_file}")
            graph = read_graph(f".\\Graphs\\{graph_file}")

            # Params:
            population_size = 50    # old 400
            chromosome_size = find_num_of_nodes(graph)
            max_colors = graphs.get(graph_file)  # chromosome_size
            genes = range(0, max_colors)
            num_generations = 2_000  # old 200_000
            num_parents_mating = 40  # old 2
            mutation_percent = 20    # old 60
            best_solution = {}
            min_conflicts = 0

            pb = ProgressBar(total=num_generations, prefix='', suffix='', decimals=3, length=50, fill='*', zfill='-')

            generation = 0
            best_colors_per_population = []
            conflicts_per_population = []
            start_time = datetime.now()
            timeout = start_time + timedelta(minutes=60)

            population = []
            # initial_population = initialize_population2(population_size, graph, genes, chromosome_size)
            initial_population = initialize_population(population_size, chromosome_size, genes)

            for _ in range(len(initial_population)):
                population.append(calculate_fitness(initial_population[_], graph))

            while (generation < num_generations) & (datetime.now() < timeout):
                if max_colors < graphs.get(graph_file):
                    break

                print("Max colors: ", max_colors, ", genes length:", len(genes))

                reduced_population = reduce_population_colors(population, genes)

                population = []
                for _ in range(len(reduced_population)):
                    population.append(calculate_fitness(reduced_population[_], graph))

                while (generation < num_generations) & (datetime.now() < timeout):

                    selected = select(population, num_parents_mating, selection_type)

                    offspring = crossover(selected, chromosome_size, crossover_type)
                    # print("offspring", offspring)
                    # mutated = mutate(offspring, mutation_percent, genes)
                    mutated = mutate2(offspring, graph, genes, mutation_percent)
                    # mutated = mutate3(offspring, graph, genes, mutation_percent)

                    new_population = []
                    for child in mutated:
                        new_population.append(calculate_fitness(child, graph))

                    print("\nbefore", count_child_size(population))
                    population = new_population + population[:population_size-len(new_population)]
                    print("\nafter", count_child_size(population))
                    population = sorted(population, key=lambda x: -x[1])
                    # count_child_size(population)
                    colors = len(set(list(population[0][0].values())))

                    pb.print_progress_bar(generation)
                    generation += 1

                    conflicts = count_greedy_conflicts(population[0][0], graph)
                    if min_conflicts != conflicts:
                        min_conflicts = conflicts
                        print("Conflicts:", min_conflicts)

                    if (colors <= max_colors) & (conflicts == 0):
                        best_solution = population[0][0]
                        best_colors_per_population.append(colors)
                        conflicts_per_population.append(conflicts)
                        break
                    else:
                        best_colors_per_population.append(colors+1)
                        conflicts_per_population.append(conflicts)

                max_colors -= 1
                genes = range(0, max_colors)

            end_time = datetime.now()
            colors = len(set(list(best_solution.values())))
            print("\nColors: {colors}".format(colors=colors))
            print("Best solution: {solution}".format(solution=best_solution))

            conflicts = 0
            if best_solution != {}:
                conflicts = count_greedy_conflicts(best_solution, graph)
            else:
                print("Best solution not found!!!")

            print("Color conflicts: {conflicts}".format(conflicts=conflicts))

            exec_time = end_time - start_time
            print("Time: {time}".format(time=exec_time))

            plots.append([graph_file, best_colors_per_population, conflicts, colors, str(exec_time), conflicts_per_population, measure_num+1])

    # Save results
    table = PrettyTable()
    table.field_names = ["Graph name", "Colors", "Conflicts", "Time"]

    excel_rows = []

    for graph in plots:
        table.add_row([f"{graph[0]} ({graph[6]})", graph[3], graph[2], graph[4]])
        excel_rows.append([f"{graph[0]} ({graph[6]})", graph[3], graph[2], graph[4]])

        plot_graph([graph[1], graph[5]], label_x="Generacja", label_y="Liczba kolorów/konfliktów",
               title="Liczba kolorów i konfliktów w stosunku do generacji", dir=f".\\plots\\{selection_type}\\{crossover_type}\\{graph[0]}\\", file_name=f"graph_{graph[0]}_{graph[6]}.png")

    df = pd.DataFrame(excel_rows, columns=["Graph name", "Colors", "Conflicts", "Time"])
    df.to_excel(f".\\plots\\{selection_type}\\{crossover_type}\\result_{time.time()}.xlsx", index=False)
    print(table)


if __name__ == '__main__':
    main()
