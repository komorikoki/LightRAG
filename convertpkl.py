import networkx as nx
import pickle
import os

INPUT_GRAPHML = "preprocessed_rag_storage_jp_v2/graph_chunk_entity_relation.graphml"
OUTPUT_PICKLE = "preprocessed_rag_storage_jp_v2/graph_chunk_entity_relation.pkl"

if not os.path.exists(INPUT_GRAPHML):
    print(f"Error: {INPUT_GRAPHML} does not exist.")
else:
    try:
        print(f"Loading graph from {INPUT_GRAPHML}...")
        G = nx.read_graphml(INPUT_GRAPHML)
        print(f"Graph loaded successfully. {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")

        with open(OUTPUT_PICKLE, "wb") as f:
            pickle.dump(G, f)
        print(f"Graph saved successfully to {OUTPUT_PICKLE}.")

    except Exception as e:
        print(f"Error: {e}")