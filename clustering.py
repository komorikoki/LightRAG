import os
import networkx as nx
import networkx.algorithms.community as nx_comm
from pyvis.network import Network

GRAPH_FILE_PATH = "./preprocessed_rag_storage/graph_chunk_entity_relation.graphml"
OUTPUT_FILENAME = "./clustered_graph.html"

def main():
    try:
        print(f"Loading graph from {GRAPH_FILE_PATH}...")
        graph = nx.read_graphml(GRAPH_FILE_PATH)
        print("Graph loaded successfully.")
    except Exception as e:
        print(f"Error loading graph: {e}")
        return

    print("starting clustering...")
    communities = list(nx_comm.greedy_modularity_communities(graph))
    print(f"Detected {len(communities)} communities.")

    net = Network(notebook=False, height="800px", width="100%", cdn_resources="in_line", directed=True)

    net.from_nx(graph)

    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    print("Assigning colors to nodes based on communities...")
    net.show_buttons(filter_=["physics", "nodes", "edges"])
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as file:
        net.generate_html()
        file.write(net.html)

if __name__ == "__main__":
    main()