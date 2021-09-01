import random


class Connection:

    def __init__(self, connection_id, from_node_id, to_node_id, enabled=True, recurrent=False):
        self.connection_id = connection_id
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.enabled = enabled
        self.recurrent = recurrent
        self.weight = None
        self.generate_new_weight()

    def generate_new_weight(self):
        self.weight = random.uniform(-1.0, 1.0)

    def set_new_weight(self, weight):
        self.weight = weight

    def mutate_weight_with_percentage(self, percentage):
        sign_value = random.choice((-1, 1))
        mutation_value = self.weight * percentage
        self.weight + (sign_value * mutation_value)
