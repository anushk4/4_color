import matplotlib.pyplot as plt

def plot_color_map(color_map,nodes_number):
    """
    Iterates through the transformed graph and replaces the initial of the color
    with the corresponding color to plot the graph
    
    Args: list (transformed graph), int (total nodes)
    
    Returns: void
    """
    color_dict = {'R': 'red', 'G': 'green', 'Y': 'yellow', 'B': 'blue'}
    rows = len(color_map)
    cols = len(color_map[0])

    # Creating a figure and axis
    fig = plt.figure("Graph")
    ax = fig.add_subplot(111)
    
    # Plotting each cell with the corresponding color
    for i in range(rows):
        for j in range(cols):
            cell_color = color_dict.get(color_map[i][j], 'white')  # Default to white if character not found
            ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, color=cell_color))

    # Set axis limits and remove ticks
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Node information printed
    plt.title("{} nodes found".format(nodes_number))

    # Display the plot
    plt.show()