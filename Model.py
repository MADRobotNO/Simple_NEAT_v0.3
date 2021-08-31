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
