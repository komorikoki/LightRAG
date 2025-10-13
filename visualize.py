import networkx as nx
from pyvis.network import Network
import webbrowser
import os

graph_file_path = "./preprocessed_rag_storage/graph_chunk_entity_relation.graphml"

try:
    g = nx.read_graphml(graph_file_path)

    net = Network(height="800px", width="100%", notebook=True, cdn_resources="in_line")
    net.from_nx(g)
    net.show_buttons(filter_=['physics'])

    html_content = net.generate_html()

    output_filename = "graph_visualization.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    full_path = os.path.abspath(output_filename)
    # webbrowser.open("file://" + full_path)

except Exception as e:
    print(f"Error: {e}")