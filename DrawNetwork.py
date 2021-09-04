import math
from Node import Node

import matplotlib.pyplot as plt

def draw_model(model, show_disabled_connections=True):
    '''
    Draw a neural network cartoon using matplotilb.

    :parameters:
        - left : float
            The center of the leftmost node(s) will be placed here
        - right : float
            The center of the rightmost node(s) will be placed here
        - bottom : float
            The center of the bottommost node(s) will be placed here
        - top : float
            The center of the topmost node(s) will be placed here
        - model : Model class
            The model of the network
    '''

    left = .07
    right = .93
    bottom = .05
    top = .95

    fig = plt.figure(figsize=(12, 12))

    '''
    - ax : matplotlib.axes.AxesSubplot
    The axes on which to plot the cartoon (get e.g. by plt.gca())
    '''
    ax = fig.gca()

    plt.axis('off')

    '''
    - layer_sizes : list of int
    List of layer sizes, including input and output dimensionality
    '''
    layer_sizes = model.get_layers_array_for_drawing()

    n_layers = len(layer_sizes)
    v_spacing = (top - bottom) / float(max(layer_sizes))
    h_spacing = (right - left) / float(len(layer_sizes) - 1)
    # Nodes

    nodes_possition = []

    for n, layer in enumerate(model.layers):
        layer_top = v_spacing * (layer.get_number_of_nodes() - 1) / 2. + (top + bottom) / 2.
        for m, node in enumerate(layer.nodes):
            node_position = [node.node_id, [n * h_spacing + left, layer_top - m * v_spacing]]
            nodes_possition.append(node_position)
            if node.node_type == Node.BIAS_NODE_TYPE:
                color = 'orange'
            else:
                color = 'w'
            circle = plt.Circle((n * h_spacing + left, layer_top - m * v_spacing), v_spacing / 6.,
                        color=color, ec='k', zorder=4)
            plt.figtext(n * h_spacing + left, layer_top - m * v_spacing, str(node.node_id), fontsize='xx-large', transform=ax.transAxes,
                        color="black", va="center", ha="center")
            ax.add_artist(circle)

    # Edges
    for layer_no, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):

        layer_top_a = v_spacing * (layer_size_a - 1) / 2. + (top + bottom) / 2.
        layer_top_b = v_spacing * (layer_size_b - 1) / 2. + (top + bottom) / 2.
        current_layer = model.get_layer_by_id(layer_no)
        next_layer = model.get_layer_by_id(layer_no + 1)
        current_layer_nodes = current_layer.get_layer_nodes()
        next_layer_nodes = next_layer.get_layer_nodes()

        for from_node in range(layer_size_a):
            current_from_node = current_layer_nodes[from_node]

            for to_node in range(layer_size_b):
                current_to_node = next_layer_nodes[to_node]

                connection = model.get_connection_by_from_to_nodes(current_from_node, current_to_node)

                if connection is None or not show_disabled_connections and not connection.enabled:
                    continue

                line = plt.Line2D([layer_no * h_spacing + left, (layer_no + 1) * h_spacing + left],
                                  [layer_top_a - from_node * v_spacing, layer_top_b - to_node * v_spacing], c='k')
                if connection.enabled and connection.weight > 0:
                    line.set_color("red")
                elif connection.enabled and connection.weight <= 0:
                    line.set_color("blue")
                elif show_disabled_connections:
                    line.set_color("grey")
                line.set_linewidth(abs(math.tanh(connection.weight))+0.5)
                ax.add_artist(line)

    fig.show()
    fig.savefig('network_graph.png')