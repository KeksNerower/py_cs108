import vkapi.friends as fr

import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx


# Creating graph
net = fr.ego_network(user_id=12345)
g = nx.Graph()
g.add_edges_from(net)

# Finding partitios
partition = community_louvain.best_partition(g)

pos = nx.spring_layout(g)
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(g, pos, partition.keys(), node_size=15,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(g, pos, alpha=0.5)

# Save graph to picture
plt.savefig("mygraph1.png")