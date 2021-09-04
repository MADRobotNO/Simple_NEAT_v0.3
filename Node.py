import numpy as np


class Node:

    NODE_TYPES = ["input", "hidden", "output", "bias"]
    INPUT_NODE_TYPE = NODE_TYPES.index("input")
    HIDDEN_NODE_TYPE = NODE_TYPES.index("hidden")
    OUTPUT_NODE_TYPE = NODE_TYPES.index("output")
    BIAS_NODE_TYPE = NODE_TYPES.index("bias")

    TANH_ACTIVATION_FUNCTION = 1
    SIGMOID_ACTIVATION_FUNCTION = 2

    def __init__(self, node_id, node_layer_id, node_type, activation_function=TANH_ACTIVATION_FUNCTION):
        self.node_id = node_id
        self.node_layer_id = node_layer_id
        self.node_type = node_type
        self.input_data = 0.
        self.output_data = 0.
        self.activation_function = activation_function

        if self.node_type == self.BIAS_NODE_TYPE:
            self.input_data = self.output_data = 1

    def node_type_to_string(self):
        return self.NODE_TYPES[self.node_type]

    def calculate_output(self):
        if self.activation_function == self.TANH_ACTIVATION_FUNCTION:
            self.output_data = np.tanh(self.input_data)
        elif self.activation_function == self.SIGMOID_ACTIVATION_FUNCTION:
            self.output_data = 1 / (1 + np.exp(-self.input_data))

    def __str__(self):
        return "Node ID: " + str(self.node_id) + ", node type: " + self.NODE_TYPES[self.node_type] \
               + ", node layer ID: " + str(self.node_layer_id) + ", input: " + str(self.input_data) \
               + ", output: " + str(self.output_data)
