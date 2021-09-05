from Node import Node

from Innovations import Innovations
from Model import Model
from DrawNetwork import draw_model

innovations = Innovations()
model = Model(0, innovations, 2, 1, bias_on_every_layer=False)

# model.connections[1].enabled = False

# for x in range(35):
#     random_num = random.randint(0, len(model.connections)-1)
#     model.connections.pop(random_num)

# node10 = model.get_node_by_id(10)
# model.remove_node(node10)

# layer = model.get_layer_by_id(2)
# node = Node(model.get_latest_node_id(), layer.layer_id, Node.HIDDEN_NODE_TYPE)
# model.add_node(node, layer, True)
model.feed_forward([0, 0])

print(model)

print(model.get_output())

draw_model(model)
