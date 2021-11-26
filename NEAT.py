import copy
import random

from Model import Model
from Species import Species
from Innovations import Innovations
from DrawNetwork import draw_model


class NEAT:
    def __init__(self, number_of_agents, number_of_generations=1, draw=True, debug=False):
        self.models = []
        self.species = []
        self.innovations = Innovations()
        self.number_of_agents = number_of_agents
        self.number_of_generations = number_of_generations

        self.number_of_input_nodes = self.number_of_output_nodes = self.number_of_hidden_layers \
            = self.number_of_hidden_nodes = 0
        self.bias_on_hidden_layers = True
        self.bias_on_first_layer = True

        self.__debug = debug
        self.__draw = draw

        self.__best_overall = None
        self.__next_model_id = 0

        # new node mutation chance
        self.__add_node_mutation_percentage = .03

        # weights mutation chances
        self.__add_connection_mutation_percentage = .1
        self.__new_weight_mutation_chance = .1
        self.__mutate_connections_by_percentage = .1
        self.__general_weight_mutation_chance = .8

        # connection mutation chances
        self.__chance_of_connection_being_added = .05
        self.__max_attempts_of_finding_connection = 20
        self.__chance_of_connection_reactivating = .25

    def set_general_weight_mutation_chance(self, percentage):
        self.__general_weight_mutation_chance = percentage

    def set_add_connection_mutation_percentage(self, percentage):
        self.__add_connection_mutation_percentage = percentage

    def set_add_node_mutation_percentage(self, percentage):
        self.__add_node_mutation_percentage = percentage

    def current_population_size(self):
        return len(self.models)

    def run(self, input_data, targets):
        self.initialize_models()
        for generation in range(self.number_of_generations):
            print("Generation:", generation)
            for index, input_data_row in enumerate(input_data):
                if self.__debug:
                    print("data row:", input_data_row, ", target:", targets[index])
                for model in self.models:
                    model.feed_forward(input_data_row)
                    model.fit_xor(targets[index])
                    if self.__debug:
                        print("model id:", model.model_id)
                        print(model.get_output())
                        print("score:", model.get_score())

            best_model = self.get_current_best_model()
            self.check_best_overall(best_model)
            print("Best score: ", best_model.get_score())

            for model in self.models:

                if self.__debug:
                    print(model)

                model.reset_score()

                # mutate weights
                if random.uniform(0., 1.) < self.__general_weight_mutation_chance:
                    if random.uniform(0., 1.) > self.__new_weight_mutation_chance:
                        model.mutate_weights(self.__mutate_connections_by_percentage)
                    else:
                        model.generate_new_weights()

                # mutate connections
                if random.uniform(0., 1.) < self.__chance_of_connection_being_added:
                    model.mutate_add_connection(self.__max_attempts_of_finding_connection,
                                                self.__chance_of_connection_reactivating)

                # mutate nodes (add node)
                if random.uniform(0., 1.) < self.__add_node_mutation_percentage:
                    model.mutate_add_node()

        best_overall = self.get_best_overall()
        print("\nBest overall: ", best_overall.get_score())
        print(best_overall)
        if self.__draw:
            draw_model(best_overall)

    def get_latest_model_id(self):
        return self.__next_model_id

    def get_best_overall(self):
        return self.__best_overall

    def check_best_overall(self, current_best):
        if self.__best_overall is None or current_best.get_score() > self.__best_overall.get_score():
            self.__best_overall = copy.deepcopy(current_best)

    def get_current_best_model(self):
        best_model = None
        for model in self.models:
            if best_model is None or model.get_score() > best_model.get_score():
                best_model = copy.deepcopy(model)
        return best_model

    def add_model(self, model):
        self.models.append(model)
        self.__next_model_id += 1

    def setup_models(self, number_of_input_nodes, number_of_output_nodes, number_of_hidden_layers,
                     number_of_hidden_nodes, bias_on_hidden_layers=True, bias_on_first_layer=True):
        self.number_of_input_nodes = number_of_input_nodes
        self.number_of_output_nodes = number_of_output_nodes
        self.number_of_hidden_layers = number_of_hidden_layers
        self.number_of_hidden_nodes = number_of_hidden_nodes
        self.bias_on_hidden_layers = bias_on_hidden_layers
        self.bias_on_first_layer = bias_on_first_layer

    def initialize_models(self):
        for x in range(len(self.models), self.number_of_agents):
            model = Model(self.get_latest_model_id(), self.innovations, self.number_of_input_nodes,
                          self.number_of_output_nodes, self.bias_on_hidden_layers, self.number_of_hidden_layers,
                          self.number_of_hidden_nodes, self.bias_on_first_layer)
            self.add_model(model)
