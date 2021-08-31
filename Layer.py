class Layer:

    LAYER_TYPES = ["input", "hidden", "output"]
    INPUT_LAYER_TYPE = LAYER_TYPES.index("input")
    HIDDEN_LAYER_TYPE = LAYER_TYPES.index("hidden")
    OUTPUT_LAYER_TYPE = LAYER_TYPES.index("output")

    def __init__(self, layer_id, layer_type):
        self.layer_id = layer_id
        self.layer_type = layer_type
        self.nodes = []
