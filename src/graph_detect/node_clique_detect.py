import networkx as nx

# Clique detection for each community
def clique_detection(G: nx.Graph, comm):
    temp_comm = comm.copy()
    list_bot = set()
    flag_exit = False
    while True:
        if len(temp_comm) < 3:
            break
        iterator = nx.clique.find_cliques(G.subgraph(temp_comm))
        set_vertex = set()
        index = 0
        while True:
            try:
                node = next(iterator)
                # print("Clique: ", node)
                if len(node) < 3:
                    if index == 0:
                        flag_exit = True
                    break
                for i in node:
                    set_vertex.add(i)
                    list_bot.add(G.nodes[i]['cls']['cls_def'][0])
                    # print("Add botnet: ", G.nodes[i]['cls']['cls_def'][0])
                index += 1
            except StopIteration:
                break
        temp_comm = temp_comm.difference(set_vertex)
        if flag_exit:
            break
    return list_bot