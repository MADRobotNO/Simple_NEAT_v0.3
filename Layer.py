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

    def get_number_of_nodes(self):
        return len(self.nodes)
