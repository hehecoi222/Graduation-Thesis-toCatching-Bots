import pickle
import os
import re

SRC_LABEL = "SrcAddr"
DST_LABEL = "DstAddr"
SPORT_LABEL = "Sport"
DPORT_LABEL = "Dport"
PROTO_LABEL = "Proto"
BPP_IN_LABEL = "BppIn"
BPP_OUT_LABEL = "BppOut"
G_BPP_IN_LABEL = "G_BppIn"
G_BPP_OUT_LABEL = "G_BppOut"

def find_cluster(flow_guid, num_clusters):
    # Check if saved clusters exist
    if not os.path.exists('out_cluster'):
        return None, -1
    
    for i in range(0, num_clusters-2):
        handle = open('out_cluster/cluster_{i}.pickle'.format(i=i), 'rb')
        cluster = pickle.load(handle)
        if flow_guid in cluster:
            handle.close()
            return cluster, i
        handle.close()
    return None, -1

def save_cluster(cluster, num_cluster):
    # Create directory if it doesn't exist
    if not os.path.exists('out_cluster'):
        os.makedirs('out_cluster')
    with open('out_cluster/cluster_{i}.pickle'.format(i=num_cluster), 'wb') as handle:
        pickle.dump(cluster, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def define_index(line):
    l = re.split(r',|\n|\t', line)
    src_index, dst_index, proto_index, bpp_in_index, bpp_out_index, g_bpp_in_index, g_bpp_out_index = -1, -1, -1, -1, -1, -1, -1
    for i, v in enumerate(l):
        if v == SRC_LABEL:
            src_index = i
        elif v == DST_LABEL:
            dst_index = i
        elif v == PROTO_LABEL:
            proto_index = i
        elif v == BPP_IN_LABEL:
            bpp_in_index = i
        elif v == BPP_OUT_LABEL:
            bpp_out_index = i
        elif v == G_BPP_IN_LABEL:
            g_bpp_in_index = i
        elif v == G_BPP_OUT_LABEL:
            g_bpp_out_index = i
    return src_index, dst_index, proto_index, bpp_in_index, bpp_out_index, g_bpp_in_index, g_bpp_out_index