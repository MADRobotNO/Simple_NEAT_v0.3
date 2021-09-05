from Model import Model
from Species import Species
from Innovations import Innovations


class NEAT:
    def __init__(self):
        self.models = []
        self.species = []
        self.innovations = Innovations()
        self.list_of_innovations = Innovations().list_of_innovations
