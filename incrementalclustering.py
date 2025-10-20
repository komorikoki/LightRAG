import cdlib.algorithms.internal_dcd.dynamic_graph as dg_mod
print(dir(dg_mod))


# import networkx as nx
# from cdlib import algorithms
# from cdlib.utils import TemporalNetwork

# PAST_GRAPH="preprocessed_rag_storage_jp_v2/graph_chunk_entity_relation.graphml"
# NEW_GRAPH="archive_rag_storage_jp_v2_part_3/graph_chunk_entity_relation.graphml"
# G_Past = nx.read_graphml(PAST_GRAPH)
# G_New = nx.read_graphml(NEW_GRAPH)

# tn = TemporalNetwork()
# tn.add_snapshot(G_Past)
# tn.add_snapshot(G_New)
# dynamic_coms = algorithms.tiles(tn)

# evolution = dynamic_coms.get_community_evolution()

# print(f"detection of community: {len(evolution)}")