from NEAT import NEAT
from RandomData import Xor

xor = Xor()
neat = NEAT(1, 20, draw=True, debug=True)
neat.setup_models(2, 1, 0, 0, False, True)
neat.set_add_node_mutation_percentage(.99)
neat.run(xor.data, xor.targets)
