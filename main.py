import copy
import time
import pandas as pd
from population import Population
from datetime import datetime, timedelta
from graph_reader import read_graph, plot_graph
from selection import roulette_wheel_selection_type, rank_selection_type, tournament_selection_type
from crossover import crossover, one_point_crossover_type, two_point_crossover_type
from mutation import mutate
from console_progressbar import ProgressBar
from prettytable import PrettyTable
from utils import find_num_of_nodes


def main():
    graphs = {
        "dimacs/fpsol2.i.1.col": 65,
        "dimacs/fpsol2.i.2.col": 30,
        "dimacs/fpsol2.i.3.col": 30,
        "dimacs/le450_15a.col": 15,
        "dimacs/le450_15b.col": 15,
        "dimacs/le450_15c.col": 15,
        "dimacs/le450_15d.col": 15,
        "dimacs/le450_25a.col": 25,
        "dimacs/le450_25b.col": 25,
        "dimacs/le450_25c.col": 25,
        "dimacs/le450_25d.col": 25,
        "dimacs/miles250.col": 8,
        "dimacs/miles500.col": 20,
        "dimacs/miles750.col": 31,
        "dimacs/miles1000.col": 42,
        "dimacs/miles1500.col": 73,
        "dimacs/mulsol.i.1.col": 49,
        "dimacs/mulsol.i.2.col": 31,
        "dimacs/mulsol.i.3.col": 31,
        "dimacs/mulsol.i.4.col": 31,
        "dimacs/mulsol.i.5.col": 31,
        "dimacs/myciel3.col": 4,
        "dimacs/myciel4.col": 5,
        "dimacs/myciel5.col": 6,
        "dimacs/myciel6.col": 7,
        "dimacs/myciel7.col": 8,
        "dimacs/queen5_5.col": 5,
        "dimacs/queen6_6.col": 7,
        "dimacs/queen7_7.col": 7,
        "dimacs/queen8_8.col": 9,
        "dimacs/queen9_9.col": 10,
        "dimacs/zeroin.i.1.col": 49,
        "dimacs/zeroin.i.2.col": 30,
        "dimacs/zeroin.i.3.col": 30,

        # Generated
        "generated/graph_generated_10_3_0.05.col": 2,
        "generated/graph_generated_10_7_0.1.col": 2,
        "generated/graph_generated_10_14_0.25.col": 3,
        "generated/graph_generated_10_24_0.5.col": 4,
        "generated/graph_generated_10_36_0.75.col": 5,
        "generated/graph_generated_10_41_0.9.col": 8,
        "generated/graph_generated_25_21_0.05.col": 3,
        "generated/graph_generated_25_29_0.1.col": 3,
        "generated/graph_generated_25_68_0.25.col": 4,
        "generated/graph_generated_25_153_0.5.col": 7,
        "generated/graph_generated_25_234_0.75.col": 11,
        "generated/graph_generated_25_273_0.9.col": 16,
        "generated/graph_generated_50_64_0.05.col": 3,
        "generated/graph_generated_50_109_0.1.col": 4,
        "generated/graph_generated_50_293_0.25.col": 7,
        "generated/graph_generated_50_621_0.5.col": 11,
        "generated/graph_generated_50_922_0.75.col": 18,
        "generated/graph_generated_50_1098_0.9.col": 25,
        "generated/graph_generated_75_128_0.05.col": 3,
        "generated/graph_generated_75_282_0.1.col": 5,
        "generated/graph_generated_75_683_0.25.col": 9,
        "generated/graph_generated_75_1376_0.5.col": 15,
        "generated/graph_generated_75_2072_0.75.col": 25,
        "generated/graph_generated_75_2513_0.9.col": 35,
        "generated/graph_generated_100_224_0.05.col": 4,
        "generated/graph_generated_100_482_0.1.col": 6,
        "generated/graph_generated_100_1193_0.25.col": 11,
        "generated/graph_generated_100_2471_0.5.col": 20,
        "generated/graph_generated_100_3725_0.75.col": 30,
        "generated/graph_generated_100_4427_0.9.col": 42,
        "generated/graph_generated_150_529_0.05.col": 4,
        "generated/graph_generated_150_1150_0.1.col": 8,
        "generated/graph_generated_150_2754_0.25.col": 15,
        "generated/graph_generated_150_5544_0.5.col": 26,
        "generated/graph_generated_150_8348_0.75.col": 46,
        "generated/graph_generated_150_10045_0.9.col": 63,
    }

    # Params:
    selection_type = tournament_selection_type
    crossover_type = two_point_crossover_type
    population_size = 150
    num_generations = 20_000
    crossover_percent = 70
    mutation_percent = 25
    num_of_measurements = 5

    plots = []
    for graph_file in graphs:
        print("\nGraph: {graphName}".format(graphName=graph_file))

        for measure_num in range(num_of_measurements):
            print(f"\nMeasurement: {measure_num + 1}/{num_of_measurements}")

            # Graph loading
            graph = read_graph(f".\\Graphs\\{graph_file}")

            pb = ProgressBar(total=num_generations, prefix='', suffix='', decimals=3, length=50, fill='*', zfill='-')

            chromosome_size = find_num_of_nodes(graph)
            max_colors = int(graphs.get(graph_file) * 3)
            genes = range(0, max_colors)
            best_solution = None
            generation = 0
            best_colors_per_population = []
            conflicts_per_population = []
            start_time = datetime.now()
            time_of_best_solution = None
            timeout = start_time + timedelta(minutes=60)

            population = Population(population_size, chromosome_size, genes, graph, selection_type=selection_type)

            while (generation < num_generations) & (datetime.now() < timeout):
                if max_colors < graphs.get(graph_file):
                    break

                population.reduce_colors(genes)

                while (generation < num_generations) & (datetime.now() < timeout):
                    # Selekcja
                    selected_chromosomes = population.select(crossover_percent)

                    # Krzyżowanie
                    offspring = crossover(selected_chromosomes)

                    # Mutacja
                    mutated = mutate(offspring, genes, mutation_percent)

                    new_population_chromosomes = mutated
                    new_population_chromosomes.extend(population.get_best_chromosomes(population_size - len(mutated)))

                    del population
                    population = Population(chromosomes=new_population_chromosomes, selection_type=selection_type)

                    current_best_solution = population.get_best_chromosomes(1)[0]
                    colors = current_best_solution.get_num_of_colors()

                    pb.print_progress_bar(generation)
                    generation += 1

                    conflicts = current_best_solution.conflicts

                    if (colors <= max_colors) & (conflicts == 0):
                        best_solution = copy.deepcopy(current_best_solution)
                        time_of_best_solution = datetime.now()
                        best_colors_per_population.append(colors)
                        conflicts_per_population.append(conflicts)
                        break
                    else:
                        best_colors_per_population.append(colors + 1)
                        conflicts_per_population.append(conflicts)

                max_colors -= 1
                genes = range(0, max_colors)

            conflicts = 0
            colors = 0
            if best_solution is not None:
                conflicts = best_solution.conflicts
                colors = best_solution.get_num_of_colors()
                print("\nBest solution: {solution}".format(solution=best_solution.chromosome))
                print("Color conflicts: {conflicts}".format(conflicts=conflicts))
                print("Colors: {colors}".format(colors=colors))
            else:
                print("\nBest solution not found!!!")

            exec_time = time_of_best_solution - start_time
            print("Time: {time}".format(time=exec_time))

            plots.append(
                [graph_file, best_colors_per_population, conflicts, colors, str(exec_time), conflicts_per_population,
                 measure_num + 1])

    # Save results
    table = PrettyTable()
    table.field_names = ["Graph name", "Colors", "Conflicts", "Time"]

    excel_rows = []

    for graph in plots:
        table.add_row([f"{graph[0]} ({graph[6]})", graph[3], graph[2], graph[4]])
        excel_rows.append([f"{graph[0]} ({graph[6]})", graph[3], graph[2], graph[4]])

        plot_graph([graph[1], graph[5]], label_x="Generacja", label_y="Liczba kolorów/konfliktów",
                   title="Liczba kolorów i konfliktów w stosunku do generacji",
                   dir=f".\\plots\\Generated\\{selection_type}\\{crossover_type}\\{graph[0]}\\",
                   file_name=f"graph_{graph[0]}_{graph[6]}.png")

    df = pd.DataFrame(excel_rows, columns=["Graph name", "Colors", "Conflicts", "Time"])
    df.to_excel(f".\\plots\\{selection_type}\\{crossover_type}\\result_{time.time()}.xlsx", index=False)
    print(table)


if __name__ == '__main__':
    main()
