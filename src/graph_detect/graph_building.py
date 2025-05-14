import networkx as nx

# Calculate ddr_i that divide dd_i by the number of dest ip
def get_len_list_ip(flows):
    set_dsts = set()
    for dst in flows:
        set_dsts.add(dst[0])
    return set_dsts

def ddr_i(ddi, dsts):
    len_dsts = len(get_len_list_ip(dsts))
    if len_dsts == 0:
        return 0
    return ddi / len_dsts

# Given 2 cluster, if they have same stats, they are a pair, then calculate MCR of 2 clusters
def mcr(cluster1, cluster2):
    cls1= cluster1['cls_def']
    cls2=cluster2['cls_def']
    
    
    # print('Evaluate between ', cls1, ' and ', cls2)
    
    # 1 is proto, 2 is bpp_in, 3 is bpp_out
    if cls1[1] != cls2[1]:
        return 0
    if cls1[2] != cls2[2]:
        return 0
    if cls1[3] != cls2[3]:
        return 0
    
    # if cls2[2] == 0:
    #     if cls1[2] != 0:
    #         return 0
    # if cls2[3] == 0:
    #     if cls1[3] != 0:
    #         return 0
    
    # if cls2[2] != 0 and not (cls1[2] / cls2[2] > 0.75 and cls1[2] / cls2[2] < 1.25):
    #     return 0
    # if cls2[3] != 0 and not (cls1[3] / cls2[3] > 0.75 and cls1[3] / cls2[3] < 1.25):
    #     return 0
    
    ip_list_1 = get_len_list_ip(cluster1['list_flows'])
    ip_list_2 = get_len_list_ip(cluster2['list_flows'])
    intersection = len(ip_list_1.intersection(ip_list_2))
    union = len(ip_list_1.union(ip_list_2))
    
    if union == 0:
        return 0
    # print('Evaluate between ', cls1, ' and ', cls2, 'with MCR: ', intersection/union, intersection, union, len(ip_list_1), len(ip_list_2))
    return intersection / union

# Main construct graph function
def construct_graph(G: nx.Graph, clusters, MCR_THRESHOLD=0.1) -> nx.Graph:
    guid_tranversed = set()
    index = 0
    total_mcr = 0
    for guid, cls in clusters.items():
        index+=1
        G.add_node(guid, cls=cls,ddr_i=ddr_i(cls['ddi'], cls['list_flows']), cls_def=cls['cls_def'])
        if index % 100 == 0:
            total_mcr = 0
        guid_tranversed.add(guid)
        for guid_j,cls_j in clusters.items():
            if guid_j in guid_tranversed:
                continue
            mcr_ij = mcr(cls, cls_j)
            total_mcr += mcr_ij
            if mcr_ij > MCR_THRESHOLD:
                G.add_edge(guid, guid_j, mcr_ij=mcr_ij)
    return G