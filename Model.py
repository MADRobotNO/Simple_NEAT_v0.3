from Connection import Connection
from Layer import Layer
from Node import Node


class Model:
    def __init__(self, model_id, innovations, number_of_input_nodes, number_of_output_nodes, number_of_hidden_layers=0,
                 number_of_hidden_nodes=0):
        self.model_id = model_id
        self.innovations = innovations
        self.number_of_input_nodes = number_of_input_nodes
        self.number_of_output_nodes = number_of_output_nodes
        self.number_of_hidden_nodes = number_of_hidden_nodes
        self.number_of_hidden_layers = number_of_hidden_layers
        self.species_id = None

        self.connections = []
        self.layers = []
        self.nodes = []

        self.initialize_model()

    def get_latest_node_id(self):
        return len(self.nodes)

    def get_latest_layer_id(self):
        return len(self.layers)

    def get_latest_connection_id(self):
        return len(self.connections)

    def initialize_model(self):
        # input layer
        input_layer = Layer(self.get_latest_layer_id(), Layer.INPUT_LAYER_TYPE)
        for x in range(self.number_of_input_nodes):
            node = Node(self.get_latest_node_id(), input_layer.layer_id, Node.INPUT_NODE_TYPE)
            self.add_node(node, input_layer)
        bias_node = Node(self.get_latest_node_id(), input_layer.layer_id, Node.BIAS_NODE_TYPE)
        self.add_node(bias_node, input_layer)
        self.add_layer(input_layer)

        # hidden layers
        for layer in range(self.number_of_hidden_layers):
            hidden_layer = Layer(self.get_latest_layer_id(), Layer.HIDDEN_LAYER_TYPE)
            for x in range(self.number_of_hidden_nodes):
                node = Node(self.get_latest_node_id(), hidden_layer.layer_id, Node.HIDDEN_NODE_TYPE)
                self.add_node(node, hidden_layer)
            self.add_layer(hidden_layer)

        # output layers
        output_layer = Layer(self.get_latest_layer_id(), Layer.OUTPUT_LAYER_TYPE)
        for x in range(self.number_of_output_nodes):
            node = Node(self.get_latest_node_id(), output_layer.layer_id, Node.OUTPUT_NODE_TYPE)
            self.add_node(node, output_layer)
        self.add_layer(output_layer)

        self.initialize_connections()

    def initialize_connections(self):
        for layer_index, layer in enumerate(self.layers):
            if layer.layer_type == layer.OUTPUT_LAYER_TYPE:
                break
            for node in layer.nodes:
                from_node_id = node.node_id
                next_layer = self.layers[layer_index + 1]
                for next_nodes in next_layer.nodes:
                    to_node_id = next_nodes.node_id
                    innovation_id = self.innovations.get_innovation_id_by_in_out_nodes(from_node_id, to_node_id)
                    connection = Connection(self.get_latest_connection_id(), innovation_id, from_node_id, to_node_id)
                    self.add_connection(connection)

    def add_node(self, node, layer):
        self.nodes.append(node)
        layer.add_node(node)

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_layer(self, layer):
        self.layers.append(layer)

    def __str__(self):
        return_string = ""
        return_string += "Model ID: " + str(self.model_id) + "\n"

        return_string += "Nodes: \n"
        for node in self.nodes:
            return_string += node.__str__() + "\n"

        return_string += "Connections: \n"
        for connection in self.connections:
            return_string += connection.__str__() + "\n"

        return_string += "Layers: \n"
        for layer in self.layers:
            return_string += layer.__str__() + "\n"

        return return_string
