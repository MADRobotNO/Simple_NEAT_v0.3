class Layer:

    LAYER_TYPES = ["input", "hidden", "output"]
    INPUT_LAYER_TYPE = LAYER_TYPES.index("input")
    HIDDEN_LAYER_TYPE = LAYER_TYPES.index("hidden")
    OUTPUT_LAYER_TYPE = LAYER_TYPES.index("output")

    def __init__(self, layer_id, layer_type):
        self.layer_id = layer_id
        self.layer_type = layer_type
        self.nodes = []

    def layer_type_to_string(self):
        return self.LAYER_TYPES[self.layer_type]

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def get_number_of_nodes(self):
        return len(self.nodes)

    def __str__(self):
        nodes_in_layer = ""
        for node in self.nodes:
            nodes_in_layer += str(node.node_id) + ", "
        return "Layer ID: " + str(self.layer_id) + ", layer type: " + self.LAYER_TYPES[self.layer_type] \
               + ", nodes in layer: " + nodes_in_layer
