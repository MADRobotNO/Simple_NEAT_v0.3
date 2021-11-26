# Singleton class
class Innovations:

    instance = None

    __next_innovation_id = 0
    list_of_innovations = []

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_innovation_id_by_in_out_node_ids(self, in_node_id, out_node_id):
        for innovation in self.list_of_innovations:
            if innovation[1][0] == in_node_id and innovation[1][1] == out_node_id:
                return innovation[0]

        self.__add_innovation(in_node_id, out_node_id)
        return self.get_next_innovation_id()

    def __add_innovation(self, in_node_id, out_node_id):
        self.list_of_innovations.append([self.get_next_innovation_id(), [in_node_id, out_node_id]])
        self.__next_innovation_id += 1

    def get_next_innovation_id(self):
        return self.__next_innovation_id

    def get_innovation_by_id(self, innovation_id):
        for innovation in self.list_of_innovations:
            if innovation[0] == innovation_id:
                return innovation

    def get_number_of_innovations(self):
        return len(self.list_of_innovations)

    def print_list_of_innovations(self):
        for innovation in self.list_of_innovations:
            self.__print_innovation(innovation[0], innovation[1])

    def print_innovation_by_id(self, innovation_id):
        innovation = self.get_innovation_by_id(innovation_id)
        self.__print_innovation(innovation[0], innovation[1])

    def __print_innovation(self, innovation_id, innovation):
        print("ID: " + str(innovation_id) + ", from: " + str(innovation[0]) + ", to: "
              + str(innovation[1]))
