import random
from Node import Node

from Innovations import Innovations
from Model import Model
from DrawNetwork import draw_neural_net

innovations = Innovations()
model = Model(0, innovations, 5, 2, 4, 3)

model.connections[1].enabled = False

# for x in range(20):
#     random_num = random.randint(0, len(model.connections)-1)
#     model.connections.pop(random_num)

node13 = model.get_node_by_id(13)
model.remove_node(node13)

layer = model.get_layer_by_id(2)
node = Node(model.get_latest_node_id(), layer.layer_id, Node.HIDDEN_NODE_TYPE)
model.add_node(node, layer, True)

print(model)

draw_neural_net(.07, .93, .05, .95, model)
