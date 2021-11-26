import math
from Node import Node
from Layer import Layer

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
            circle = plt.Circle((n * h_spacing + left, layer_top - m * v_spacing), v_spacing / 8.,
                        color=color, ec='k', zorder=4)
            plt.figtext(n * h_spacing + left, layer_top - m * v_spacing, str(node.node_id), fontsize='xx-large', transform=ax.transAxes,
                        color="black", va="center", ha="center")
            ax.add_artist(circle)

    # Edges
    for layer_no, layer_size in enumerate(layer_sizes):

        current_layer = model.get_layer_by_id(layer_no)
        if current_layer.layer_type == Layer.OUTPUT_LAYER_TYPE:
            continue
        current_layer_nodes = current_layer.get_layer_nodes()

        for from_node in current_layer_nodes:

            for to_node in model.nodes:
                connection = model.get_connection_by_from_to_nodes(from_node, to_node)
                if connection is None or not show_disabled_connections and not connection.enabled:
                    continue

                from_node_position = []
                to_node_position = []
                for position in nodes_possition:

                    if position[0] == from_node.node_id:
                        from_node_position = position[1]
                    elif position[0] == to_node.node_id:
                        to_node_position = position[1]
                line = plt.Line2D([from_node_position[0], to_node_position[0]], [from_node_position[1], to_node_position[1]])
                ax.add_artist(line)

    fig.show()
    fig.savefig('network_graph.png')