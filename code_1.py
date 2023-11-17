import sys
import matplotlib.pyplot as plt

def plot_color_map(color_map):
    color_dict = {'R': 'red', 'G': 'green', 'Y': 'yellow', 'B': 'blue'}

    rows = len(color_map)
    cols = len(color_map[0])

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot each cell with the corresponding color
    for i in range(rows):
        for j in range(cols):
            cell_color = color_dict.get(color_map[i][j], 'white')  # Default to white if character not found
            ax.add_patch(plt.Rectangle((j, rows - i - 1), 1, 1, color=cell_color))

    # Set axis limits and remove ticks
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])

    # Display the plot
    plt.show()

def check_node(x,y,prev,queue,nodes):
    if x < 0 or y < 0:
        return
    try:
        if isinstance(nodes[x][y], int) and nodes[x][y] == prev:
            queue.append((x, y))
    except:
        pass

def fill_color(i, j, nodes,color):
    queue = [(i, j)]
    while queue != []:
        p = queue.pop()
        prev_value = nodes[p[0]][p[1]]
        nodes[p[0]][p[1]] = color
        check_node(p[0],p[1] + 1, prev_value,queue, nodes)
        check_node(p[0],p[1] - 1, prev_value,queue, nodes)
        check_node(p[0] + 1,p[1], prev_value,queue, nodes)
        check_node(p[0] -  1,p[1], prev_value,queue, nodes)

def check_existing_color(x, y, queue, nodes, na_colors,val,checked):
    if (x,y) in checked:
        return
    if x < 0 or y < 0:
        return
    try:
        if nodes[x][y] == val:
            queue.append((x,y))
        else:
            if isinstance(nodes[x][y],str):
                na_colors.append(nodes[x][y])
    except:
        pass

def check_neighbour_color(x,y,nodes,na_colors):
    queue = [(x,y)]
    checked = []
    while queue != []:
        p = queue.pop()
        val = nodes[p[0]][p[1]]
        check_existing_color(p[0],p[1] + 1,queue,nodes,na_colors,val,checked)
        check_existing_color(p[0],p[1] - 1,queue,nodes,na_colors,val,checked)
        check_existing_color(p[0] + 1,p[1],queue,nodes,na_colors,val,checked)
        check_existing_color(p[0] - 1,p[1],queue,nodes,na_colors,val,checked)
        checked.append(p)
 
def find_unused_color(colors,na_color):
    for i in colors:
        if i not in na_color:
            return i
    print("Something went wrong")
    sys.exit(1)

def find_nodes(nodes):
    global colors
    global nodes_number
    fill_color(0, 0, nodes,colors[0])
    na_colors = []
    nodes_number += 1
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            if isinstance(nodes[i][j],str):
                continue
            check_neighbour_color(i,j,nodes,na_colors)
            na_colors = list(set(na_colors))
            color = find_unused_color(colors,na_colors)
            fill_color(i, j, nodes,color)
            nodes_number += 1
            na_colors = []
    print("{} nodes found".format(nodes_number))
            
file = open("input.txt","r")
node = file.readlines()
node = [list(map(int,list(i.strip("\n")))) for i in node]
nodes_number = 0
output = node.copy()
colors = ["R","G","B","Y"]
find_nodes(output)
for i in output:
    print("".join(list(map(str,i))))
output = ["".join(list(map(str,i))) for i in output]
plot_color_map(output)
file.close()