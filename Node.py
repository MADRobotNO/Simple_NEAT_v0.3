class Node:

    NODE_TYPES = ["input", "hidden", "output"]
    INPUT_NODE_TYPE = NODE_TYPES.index("input")
    HIDDEN_NODE_TYPE = NODE_TYPES.index("hidden")
    OUTPUT_NODE_TYPE = NODE_TYPES.index("output")

    def __init__(self, node_id, node_layer_id, node_type):
        self.node_id = node_id
        self.node_layer_id = node_layer_id
        self.node_type = node_type

    def node_type_to_string(self):
        return self.NODE_TYPES[self.node_type]
