import random

from Connection import Connection
from Layer import Layer
from Node import Node


class Model:
    def __init__(self, model_id, innovations, number_of_input_nodes, number_of_output_nodes, bias_on_hidden_layers,
                 number_of_hidden_layers=0, number_of_hidden_nodes=0, bias_on_first_layer=True):
        self.model_id = model_id
        self.innovations = innovations
        self.number_of_input_nodes = number_of_input_nodes
        self.number_of_output_nodes = number_of_output_nodes
        self.number_of_hidden_nodes = number_of_hidden_nodes
        self.number_of_hidden_layers = number_of_hidden_layers
        self.species_id = None
        self.bias_on_hidden_layers = bias_on_hidden_layers
        self.bias_on_first_layer = bias_on_first_layer
        self.__output = []

        self.connections = []
        self.layers = []
        self.nodes = []

        self.__next_node_id = 0
        self.__next_layer_id = 0
        self.__next_connection_id = 0

        self.__score = 0.0

        self.initialize_model()

    def fit_xor(self, targets):
        for index, output in enumerate(self.__output):
            error = abs(targets - output)
            if error > 0.5:
                error = 1
            score = 1 - error
            self.__score += score

    def get_score(self):
        return self.__score

    def reset_score(self):
        self.__score = 0.0

    def feed_forward(self, input_data):
        if self.number_of_input_nodes != len(input_data):
            return None

        self.load_input_data(input_data)

        for layer in self.layers:
            if layer.layer_id == 0:
                continue
            for node in layer.nodes:
                if node.node_type == Node.BIAS_NODE_TYPE:
                    continue

                connections = self.get_connections_by_to_node(node)

                node_input_value = 0.0
                for connection in connections:
                    input_value = self.get_node_by_id(connection.from_node_id).output_data
                    node_input_value += input_value * connection.weight
                node.input_data = node_input_value
                node.calculate_output()

        self.__set_output()

    def get_output(self):
        return self.__output

    def __set_output(self):
        self.__output = []
        for layer in self.layers:
            if layer.layer_type != Layer.OUTPUT_LAYER_TYPE:
                continue
            for output_node in layer.nodes:
                self.__output.append(output_node.output_data)

    def load_input_data(self, input_data):
        loaded_data_nodes = 0
        for input_node in self.nodes:
            if input_node.node_type == Node.INPUT_NODE_TYPE:
                input_node.input_data = input_node.output_data = input_data[input_node.node_id]
                loaded_data_nodes += 1
            if loaded_data_nodes == len(input_data):
                break

    def get_latest_node_id(self):
        return self.__next_node_id

    def get_latest_layer_id(self):
        return self.__next_layer_id

    def get_latest_connection_id(self):
        return self.__next_connection_id

    def get_layer_by_node(self, node):
        for layer in self.layers:
            if node in layer.nodes:
                return layer

    def get_all_connections_by_node(self, node):
        node_connections = []
        for connection in self.connections:
            if connection.from_node_id == node.node_id or connection.to_node_id == node.node_id:
                node_connections.append(connection)
        return node_connections

    def get_all_active_connections_by_node(self, node):
        node_connections = []
        for connection in self.connections:
            if connection.from_node_id == node.node_id or connection.to_node_id == node.node_id and connection.enabled:
                node_connections.append(connection)
        return node_connections

    def get_connections_by_to_node(self, to_node):
        node_connections = []
        for connection in self.connections:
            if connection.to_node_id == to_node.node_id and connection.enabled:
                node_connections.append(connection)
        return node_connections

    def get_connection_by_from_to_nodes(self, from_node, to_node):
        for connection in self.connections:
            if connection.from_node_id == from_node.node_id and connection.to_node_id == to_node.node_id and connection.enabled:
                return connection
        return None

    def remove_node(self, node):
        layer = self.get_layer_by_node(node)
        layer.remove_node(node)
        self.nodes.remove(node)
        connections = self.get_all_connections_by_node(node)
        for connection in connections:
            connection.enabled = False

    def initialize_model(self):
        # input layer
        input_layer = Layer(self.get_latest_layer_id(), Layer.INPUT_LAYER_TYPE)
        for x in range(self.number_of_input_nodes):
            node = Node(self.get_latest_node_id(), input_layer.layer_id, Node.INPUT_NODE_TYPE)
            self.add_node(node, input_layer)
        if self.bias_on_first_layer:
            bias_node = Node(self.get_latest_node_id(), input_layer.layer_id, Node.BIAS_NODE_TYPE)
            self.add_node(bias_node, input_layer)
        self.add_layer(input_layer)

        # hidden layers
        for layer in range(self.number_of_hidden_layers):
            hidden_layer = Layer(self.get_latest_layer_id(), Layer.HIDDEN_LAYER_TYPE)
            for x in range(self.number_of_hidden_nodes):
                node = Node(self.get_latest_node_id(), hidden_layer.layer_id, Node.HIDDEN_NODE_TYPE)
                self.add_node(node, hidden_layer)
            if self.bias_on_hidden_layers:
                bias_node = Node(self.get_latest_node_id(), hidden_layer.layer_id, Node.BIAS_NODE_TYPE)
                self.add_node(bias_node, hidden_layer)
            self.add_layer(hidden_layer)

        # output layers
        output_layer = Layer(self.get_latest_layer_id(), Layer.OUTPUT_LAYER_TYPE)
        for x in range(self.number_of_output_nodes):
            node = Node(self.get_latest_node_id(), output_layer.layer_id, Node.OUTPUT_NODE_TYPE,
                        Node.SIGMOID_ACTIVATION_FUNCTION)
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
                    innovation_id = self.innovations.get_innovation_id_by_in_out_node_ids(from_node_id, to_node_id)
                    connection = Connection(self.get_latest_connection_id(), innovation_id, from_node_id, to_node_id)
                    self.add_connection(connection)

    def add_node(self, node, layer, add_connections=False):
        self.nodes.append(node)
        layer.add_node(node)
        self.__next_node_id += 1

        if add_connections:
            layer_id = layer.layer_id
            previous_layer = self.get_layer_by_id(layer_id-1)
            for from_node in previous_layer.nodes:
                connection = Connection(self.get_latest_connection_id(),
                                        self.innovations.get_innovation_id_by_in_out_node_ids(from_node.node_id,
                                                                                              node.node_id),
                                        from_node.node_id, node.node_id)
                self.add_connection(connection)
            next_layer = self.get_layer_by_id(layer.layer_id+1)
            for to_node in next_layer.nodes:
                connection = Connection(self.get_latest_connection_id(),
                                        self.innovations.get_innovation_id_by_in_out_node_ids(node.node_id,
                                                                                              to_node.node_id),
                                        node.node_id, to_node.node_id)
                self.add_connection(connection)

    def mutate_add_node(self):
        connection = self.select_connection_to_add_node()
        connection.enabled = False
        old_weight = connection.weight
        connection_to_node = self.get_node_by_id(connection.to_node_id)
        connection_from_node = self.get_node_by_id(connection.from_node_id)
        new_node = Node(self.get_latest_node_id(), connection_to_node.node_layer_id, Node.HIDDEN_NODE_TYPE,
                        connection_to_node.activation_function)
        layer = self.get_layer_by_id(connection_to_node.node_layer_id)
        self.add_node(new_node, layer)
        from_connection_innovation_id = self.innovations.get_innovation_id_by_in_out_node_ids(connection_from_node.
                                                                                              node_id, new_node.node_id)
        from_connection = Connection(self.get_latest_connection_id(), from_connection_innovation_id,
                                     connection_from_node.node_id, new_node.node_id)
        from_connection.weight = old_weight
        self.add_connection(from_connection)
        to_connection_innovation_id = self.innovations.get_innovation_id_by_in_out_node_ids(new_node.node_id,
                                                                                            connection_to_node.node_id)
        to_connection = Connection(self.get_latest_connection_id(), to_connection_innovation_id, new_node.node_id,
                                   connection_to_node.node_id)
        self.add_connection(to_connection)

        self.reasign_nodes_to_layers()

        # TODO: ADD LAYER CLEANING
    def reasign_nodes_to_layers(self):
        for node in self.nodes:
            new_layer_id = self.get_node_layer_position(node)
            new_layer = self.get_layer_by_id(new_layer_id)
            if new_layer is None:
                old_layer = self.get_layer_by_id(self.get_latest_layer_id()-1)
                old_layer.layer_type = Layer.HIDDEN_LAYER_TYPE
                new_layer = Layer(self.get_latest_layer_id(), Layer.OUTPUT_LAYER_TYPE)
                self.add_layer(new_layer)
            if node.node_layer_id != new_layer.layer_id:
                self.move_node_to_layer(node, new_layer)

    def get_node_layer_position(self, node, position=0):
        if node.node_layer_id == 0:
            return position
        else:
            connections = self.get_connections_by_to_node(node)
            lengst_position = 0
            for connection in connections:
                node = self.get_node_by_id(connection.from_node_id)
                current_position = self.get_node_layer_position(node, position + 1)
                if current_position > lengst_position:
                    lengst_position = current_position
            return lengst_position

    def select_connection_to_add_node(self):
        connection = self.connections[random.randint(0, len(self.connections)-1)]
        while not connection.enabled:
            connection = self.connections[random.randint(0, len(self.connections)-1)]
        return connection

    def mutate_add_connection(self, max_attempts_of_finding_connection, chance_of_connection_reactivating):
        returned_nodes = None
        for number_of_attempts in range(max_attempts_of_finding_connection):
            returned_nodes = self.__select_from_to_nodes(max_attempts_of_finding_connection)

            if returned_nodes is None:
                # print("Cannot select nodes")
                return None

            connection = self.get_connection_by_from_to_nodes(returned_nodes[0], returned_nodes[1])

            if connection is not None:
                if not connection.enabled and random.uniform(0., 1.) < chance_of_connection_reactivating:
                    connection.enabled = True
                    return None
                else:
                    number_of_attempts += 1
                    continue
            else:
                break

        from_node = returned_nodes[0]
        to_node = returned_nodes[1]

        innovation_id = self.innovations.get_innovation_id_by_in_out_node_ids(from_node.node_id, to_node.node_id)
        new_connection = Connection(self.get_latest_connection_id(), innovation_id, from_node.node_id, to_node.node_id)
        self.add_connection(new_connection)

    def __select_from_to_nodes(self, max_attempts_of_finding_connection):
        from_node = self.get_node_by_id(random.randint(0, len(self.nodes)-1))

        while from_node.node_type == Node.OUTPUT_NODE_TYPE:
            from_node = self.get_node_by_id(random.randint(0, len(self.nodes)-1))

        to_node = self.get_node_by_id(random.randint(0, len(self.nodes)-1))

        number_of_attempts = 0
        while from_node.node_id == to_node.node_id or from_node.node_layer_id >= to_node.node_layer_id:
            if number_of_attempts < max_attempts_of_finding_connection:
                # print("NUMBER OF ATTEMPTS EXCEEDED 20")
                return None
            to_node = self.get_node_by_id(random.randint(0, len(self.nodes)-1))
            number_of_attempts += 1

        return [from_node, to_node]

    def mutate_weights(self, percentage=None):
        for connection in self.connections:
            connection.mutate_weight_with_percentage(percentage)

    def generate_new_weights(self):
        for connection in self.connections:
            connection.generate_new_weight()

    def add_connection(self, connection):
        self.connections.append(connection)
        self.__next_connection_id += 1

    def add_layer(self, layer):
        self.layers.append(layer)
        self.__next_layer_id += 1

    def get_connection_by_id(self, connection_id):
        for connection in self.connections:
            if connection.connection_id == connection_id:
                return connection

    def get_layer_by_id(self, layer_id):
        for layer in self.layers:
            if layer.layer_id == layer_id:
                return layer

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def get_layers_array_for_drawing(self):
        layers_array = []
        for layer in self.layers:
            layers_array.append(layer.get_number_of_nodes())
        return layers_array

    def move_node_to_layer(self, node, layer):
        current_layer = self.get_layer_by_id(node.node_layer_id)
        current_layer.remove_node(node)
        layer.add_node(node)
        node.node_layer_id = layer.layer_id

    def __str__(self):
        return_string = ""
        return_string += "Model ID: " + str(self.model_id) + "\n"
        return_string += "Species ID: " + str(self.species_id) + "\n"
        return_string += "Score: " + str(self.__score) + "\n"

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
