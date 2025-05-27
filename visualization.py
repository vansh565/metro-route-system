import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph, path=None, start=None, end=None, output_path="D:\metro routing system project daa\static\graph.png"):
    plt.clf() 
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    node_colors = ['lightblue' if node not in [start, end] else 'green' if node == start else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=12, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)

    plt.title("Metro Routing: Shortest Path", fontsize=14)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close() 