class Node:

    NODE_TYPES = ["input", "hidden", "output", "bias"]
    INPUT_NODE_TYPE = NODE_TYPES.index("input")
    HIDDEN_NODE_TYPE = NODE_TYPES.index("hidden")
    OUTPUT_NODE_TYPE = NODE_TYPES.index("output")
    BIAS_NODE_TYPE = NODE_TYPES.index("bias")

    def __init__(self, node_id, node_layer_id, node_type):
        self.node_id = node_id
        self.node_layer_id = node_layer_id
        self.node_type = node_type

    def node_type_to_string(self):
        return self.NODE_TYPES[self.node_type]

    def __str__(self):
        return "Node ID: " + str(self.node_id) + ", node type: " + self.NODE_TYPES[self.node_type] \
               + ", node layer ID: " + str(self.node_layer_id)
