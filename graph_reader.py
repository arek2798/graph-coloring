import matplotlib.pyplot as plt
import os


def read_graph(file_name):
    graph = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 3:
                    line_type, vertex1, vertex2 = parts

                    if line_type == 'e':
                        if int(vertex1) in graph:
                            graph[int(vertex1)].append(int(vertex2))
                        else:
                            graph[int(vertex1)] = [int(vertex2)]

        print(f"Graph {file_name} loaded.")
        return graph
    except FileNotFoundError:
        print(f"File {file_name} does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def plot_graph(data, title="Wykres danych", label_x="Oś X", label_y="Oś Y", save=True, dir="", file_name="graph.png"):
    plt.plot(data[0], color='g', label='colors')
    plt.plot(data[1], color='r', label='conflicts')

    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend()

    if save:
        if not os.path.isdir(dir):
            os.makedirs(dir)

        plt.savefig(dir+file_name)

    plt.clf()
