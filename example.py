import random

from Innovations import Innovations
from Model import Model
from DrawNetwork import draw_neural_net

innovations = Innovations()
model = Model(0, innovations, 2, 1, 5, 4)
model.connections[1].enabled = False
# for x in range(40):
#     random_num = random.randint(0, len(model.connections)-1)
#     model.connections.pop(random_num)

node13 = model.get_node_by_id(13)
model.remove_node(node13)
print(model)

draw_neural_net(.07, .93, .05, .95, model)