import networkx as nx
from graph_detect.node_clique_detect import clique_detection

# Louvain community detection
def louvain_community_detection(G):
    return nx.community.louvain_communities(G, weight='mcr_ij')

# Evaluate community and output botnet list, include check comm mcr with threshold, cliques detection
def evaluate_community(G, new_way=True, AVG_DD_THRESHOLD=0.3, AVG_MCR_THRESHOLD=0.1):
    comm_set = louvain_community_detection(G)
    print('Evaluate community', len(comm_set))
    list_bot = set()
    bot_comm = []
    for comm in comm_set:
        total_ddri = 0
        if len(comm) == 0:
            continue
        for index in comm:
            total_ddri += G.nodes[index]['ddr_i']
        avg_ddri = total_ddri / len(comm)
        if avg_ddri < AVG_DD_THRESHOLD:
            # Implement no botnet flag
            continue
        
        total_mcr = 0
        edges = G.edges(comm)
        if len(edges) == 0:
            continue
        for edge in edges:
            total_mcr += G[edge[0]][edge[1]]['mcr_ij']
        avg_mcr = (2 * total_mcr) / (len(comm) * (len(comm)-1) )
        it = iter(comm)
        # print('Evaluate Community:', G.nodes[next(it)]['cls']['cls_def'], ', with avg_mcr:', avg_mcr, "avg_ddri:", avg_ddri)
        if avg_mcr < AVG_MCR_THRESHOLD:
            # Implement no botnet flag
            continue
        bot_comm.append(comm)
        
    print('Botnet community', len(bot_comm))
    
    if not new_way:
        for comm in bot_comm:
            for node in comm:
                list_bot.add(G.nodes[node]['cls']['cls_def'][0])
                # print("Add botnet: ", G.nodes[node]['cls']['cls_def'][0])
    else:    
        for comm in bot_comm:
            list_bot.update(clique_detection(G, comm))
        
    return list_bot