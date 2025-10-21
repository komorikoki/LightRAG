import networkx as nx
import community as community_louvain
from collections import defaultdict
from pyvis.network import Network
import random

PAST_GRAPH = "preprocessed_rag_storage_jp_v2/graph_chunk_entity_relation.graphml"
NEW_GRAPH = "archive_rag_storage_jp_v2_part_3/graph_chunk_entity_relation.graphml"

def louvain_partition(graph):
    partition = community_louvain.best_partition(graph)
    return partition

def invert_partition(partition):
    inv = defaultdict(set)
    for n, cid in partition.items():
        inv[cid].add(n)
    return dict(inv)

def detect_changes(G_past, G_new):
    nodes_p = set(G_past.nodes())
    nodes_n = set(G_new.nodes())

    nodes_added = nodes_n - nodes_p
    nodes_removed = nodes_p - nodes_n

    edges_p = set(tuple(sorted(e)) for e in G_past.edges())
    edges_n = set(tuple(sorted(e)) for e in G_new.edges())

    edges_added = edges_n - edges_p
    edges_removed = edges_p - edges_n

    changed_nodes = set(nodes_added) | set(nodes_removed)
    for u, v in edges_added | edges_removed:
        changed_nodes.add(u)
        changed_nodes.add(v)
    
    return {
        "nodes_added": nodes_added,
        "nodes_removed": nodes_removed,
        "edges_added": edges_added,
        "edges_removed": edges_removed,
        "changed_nodes": changed_nodes
    }

def expand_by_hops(G, seeds, hops=1, max_nodes=None):
    visited = set(seeds)
    frontier = set(seeds)

    for _ in range(hops):
        next_front = set()
        for n in frontier:
            nbrs = set(G.neighbors(n))
            next_front |= (nbrs - visited)
        if not next_front:
            break
        visited |= next_front
        frontier = next_front
        if max_nodes and len(visited) >= max_nodes:
            break
    return visited

G_Past = nx.read_graphml(PAST_GRAPH)
G_New = nx.read_graphml(NEW_GRAPH)

past_partition = louvain_partition(G_Past)
past_inv = invert_partition(past_partition)

diff = detect_changes(G_Past, G_New)
changed = diff["changed_nodes"]

print(f"Number of changed nodes: {len(changed)}")

if len(changed) == 0:
    new_partition = {n: past_partition[n] for n in G_New.nodes() if n in past_partition}
else:
    H_nodes = expand_by_hops(G_New, changed, hops=1)
    H = G_New.subgraph(H_nodes).copy()
    local_partition = louvain_partition(H)
    
    max_past_cid = max(past_inv.keys()) if past_inv else -1
    next_cid = max_past_cid + 1

    new_partition = {}

    for n in G_New.nodes():
        if n not in H_nodes:
            if n in past_partition:
                new_partition[n] = past_partition[n]
            else:
                new_partition[n] = next_cid
                next_cid += 1
    
    local_to_global = {}

    for node, local_cid in local_partition.items():
        if local_cid not in local_to_global:
            local_to_global[local_cid] = next_cid
            next_cid += 1
        new_partition[node] = local_to_global[local_cid]


print(f"Total communities in new partition: {len(set(new_partition.values()))}")
print(f"nodes in new_partition: {len(new_partition)} (nodes in G_New: {G_New.number_of_nodes()})")

com_ids = set(past_partition.values())
palette = {cid: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for cid in com_ids}

net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="#343434", directed=True)
net.force_atlas_2based()

for node in G_Past.nodes():
    cid = past_partition[node]
    net.add_node(node, label=str(node), color=palette[cid], title=f"Community {cid}")

for u, v in G_Past.edges():
    net.add_edge(u, v)

html = net.generate_html()    # ← これで HTML を文字列として取得
with open("G_Past_louvain.html", "w", encoding="utf-8") as f:
    f.write(html)

com_ids = set(new_partition.values())
palette = {cid: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for cid in com_ids}
net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="#343434", directed=True)
net.force_atlas_2based()

for node in G_New.nodes():
    cid = new_partition[node]
    net.add_node(node, label=str(node), color=palette[cid], title=f"Community {cid}")

for u, v in G_New.edges():
    net.add_edge(u, v)

html = net.generate_html()    # ← これで HTML を文字列として取得
with open("G_New_louvain.html", "w", encoding="utf-8") as f:
    f.write(html)