import os
import tkinter as tk
from tkinter import messagebox
import map_color

def check_node(x,y,prev,queue,nodes):
    """
    Checks if the point is uncolored and is equal to the value of the original point
    Checks if the point is part of the node that is to be colored
    
    Args: int (row number), int (column number), int (value of the node), list (queue for BFS), 
    nested list (graph)
    
    Returns: void
    """
    if x < 0 or y < 0:
        return
    try:
        # Adds the point to the queue if it is uncolored and part of the node
        if isinstance(nodes[x][y], int) and nodes[x][y] == prev:
            queue.append((x, y))
    except:
        pass

def fill_color(i, j, nodes,color):
    """
    Follows the flood fill algorithm based on BFS to replace the integer value with
    the passed color value. Fills the entire node with one single color
    
    Args: int (row number), int (column number), nested list (graph), string (color)
    
    Returns: void
    """
    queue = [(i, j)]
    while queue != []:
        p = queue.pop()
        prev_value = nodes[p[0]][p[1]]
        nodes[p[0]][p[1]] = color
        check_node(p[0], p[1] + 1, prev_value,queue, nodes)
        check_node(p[0], p[1] - 1, prev_value,queue, nodes)
        check_node(p[0] + 1, p[1], prev_value,queue, nodes)
        check_node(p[0] -  1, p[1], prev_value,queue, nodes)

def check_existing_color(x, y, queue, nodes, na_colors,val,checked):
    """
    Checks the marginal points of the node to find out the unused color
    If the marginal point is colored, then it is added to a list and if it is a part of the node,
    it is added back to the queue to check through BFS
    
    Args: int (row), int (column), list (queue for BFS), nested list (graph), 
    list (unavailable colors), int (value of the node), list (nodes that have been visited)
    
    Returns: void
    """
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
    """
    Applies BFS to the point to find out available colors to be used for coloring that node
    
    Args: int (row), int (column), nested list (graph), list (unavailable colors)
    
    Returns: void
    """
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
    """
    Iterates through the colors available and returns the first unused color by checking from na_colors
    
    Args: list (possible colors), list (unavailable colors)
    
    Returns: string (unused color)
    """
    for i in colors:
        if i not in na_color:
            return i

def find_nodes(nodes):
    """
    Iterates through all points in graph, finds the available color and fills the color
    into the graph through BFS
    
    Args: nested list (graph)
    
    Returns: void
    """
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
            
def on_button_click():
    """
    Gets the input, opens the file in read mode and iterates through the file
    to store the data in form of a nested list. The modified graph is then plotted
    and node numbers are reset
    
    Args: void
    
    Returns: void
    """
    try:
        input_text = file_entry.get()
        file = open(os.path.join("test_cases",input_text),"r")
    except:
        # File not found exception
        prompt_message = "{} is not found in the test_cases directory".format(input_text)
        messagebox.showerror("File Not Found",prompt_message)
        app.destroy()
    data = file.readlines()
    if not data:
        # Empty file found
        prompt_message = "No data in {}".format(input_text)
        messagebox.showerror("No data found",prompt_message)
        app.destroy()
    nodes = [list(map(int, list(line.strip("\n")))) for line in data]
    global nodes_number
    output = nodes.copy()
    find_nodes(output)
    output = ["".join(list(map(str, i))) for i in output]
    map_color.plot_color_map(output,nodes_number)
    nodes_number = 0

# initialising the values required
colors = ["R", "G", "B", "Y"]  
nodes_number = 0   
       
app = tk.Tk()
app.title("Graph Coloring")

# Creating a label for user instruction
label = tk.Label(app, text="Enter file name:")
label.pack(pady=10)

# Creating an entry for file input
file_entry = tk.Entry(app, width=50)
file_entry.pack(pady=(0, 10), padx=10)

# Creating a button to trigger the graph display
button = tk.Button(app, text="Generate Graph", command=on_button_click)
button.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()