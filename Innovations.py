# Singleton class
class Innovations:

    instance = None

    list_of_innovations = []

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_innovation_id_by_in_out_node_ids(self, in_node, out_node):
        for innovation_index, innovation in enumerate(self.list_of_innovations):
            if innovation[0] == in_node and innovation[1] == out_node:
                return innovation_index

        self.__add_innovation(in_node, out_node)
        return self.get_last_innovation_id()

    def __add_innovation(self, in_node, out_node):
        self.list_of_innovations.append([in_node, out_node])

    def get_last_innovation_id(self):
        return len(self.list_of_innovations)-1

    def get_innovation_by_id(self, innovation_id):
        return self.list_of_innovations[innovation_id]

    def get_number_of_innovations(self):
        return len(self.list_of_innovations)

    def print_list_of_innovations(self):
        for innovation_index, innovation in enumerate(self.list_of_innovations):
            self.__print_innovation(innovation_index, innovation)

    def print_innovation_by_id(self, innovation_id):
        innovation = self.list_of_innovations[innovation_id]
        self.__print_innovation(innovation_id, innovation)

    def __print_innovation(self, innovation_id, innovation):
        print("ID: " + str(innovation_id) + ", from: " + str(innovation[0]) + ", to: "
              + str(innovation[1]))
