import ipaddress
import re
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from p2p_clustering.file_handling import define_index

ADDR_LABEL = "Addr"
TYPE_LABEL = "Type"

def get_scores(flow_files, bots_ip_files, local_subnet, bots_set):
    # Define mapping
    mapping = set()
    info_bots = set()
    
    src_index, dst_index = 0, 0

    # Read file -> get all IPs
    if isinstance(flow_files, list) or isinstance(flow_files, set):
        for ip in flow_files:
            mapping.add(ip)
    else:
        with open(flow_files) as f:
            l_index = 0
            for line in f:
                # If first line (header)
                if (l_index == 0):
                    src_index, dst_index, _, _, _, _, _ = define_index(line)
                    l_index += 1
                    continue
                
                # Split line into list
                l = re.split(r',|\t|\n', line)
                mapping.add(l[src_index])
                mapping.add(l[dst_index])

    if isinstance(bots_ip_files, list) or isinstance(bots_ip_files, set):
        for ip in bots_ip_files:
            info_bots.add(ip)
    else:
        with open(bots_ip_files) as f:
            l_index = 0
            addr_index, type_index = 0, 0
            for line in f:
                l = re.split(r',|\n|\t| ', line)
                if (l_index == 0):
                    for v in l:
                        if v == ADDR_LABEL:
                            addr_index = l.index(v)
                        elif v == TYPE_LABEL:
                            type_index = l.index(v)
                    l_index += 1
                    continue
                
                try:
                    if ipaddress.ip_address(l[addr_index]):
                        info_bots.add(l[addr_index])
                except ValueError:
                    print(f"Invalid IP address: {l[addr_index]}")
                    pass

    temp_mapping = set(mapping)
    # Remove publics IP in mapping
    for ip in mapping:
        try:
            if ipaddress.ip_address(ip) not in ipaddress.ip_network(local_subnet, strict=False):
                temp_mapping.remove(ip)
        except ValueError:
            temp_mapping.remove(ip)
    mapping = temp_mapping
    
    # True Positive 
    number_tp_list = (info_bots.intersection(bots_set))
    number_tp = len(number_tp_list)

    # True Negative 
    number_tn_list = (mapping.difference(info_bots)).intersection(mapping.difference(bots_set))
    number_tn = len(number_tn_list)

    # False Positive 
    number_fp_list = (bots_set.difference(info_bots))
    number_fp = len(number_fp_list)

    # False Negative 
    number_fn_list = (info_bots.difference(bots_set))
    number_fn = len(number_fn_list)

    precision = number_tp / (number_tp + number_fp) if (number_tp + number_fp) != 0 else 0
    recall = number_tp / (number_tp + number_fn) if (number_tp + number_fn) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    return precision, recall, f1_score, [[number_tp, number_fp], [number_fn, number_tn]]

def return_mapping(flow_files, mapping_files):
    # Define mapping
    mapping = set()
    with_mapping = set()
    mapper = {}
    
    src_index, dst_index = 0, 0
    with open(flow_files) as f:
        l_index = 0
        for line in f:
            # If first line (header)
            if (l_index == 0):
                src_index, dst_index, _, _, _, _, _ = define_index(line)
                l_index += 1
                continue
            
            # Split line into list
            l = re.split(r',|\t|\n| ', line)
            mapping.add(l[src_index])
            mapping.add(l[dst_index])
            
    addr_index, type_index = -1, -1
    with open(mapping_files) as f:
        l_index = 0
        for line in f:
            l = re.split(r',|\n|\t| ', line)
            if (l_index == 0):
                for v in l:
                    if v == ADDR_LABEL:
                        addr_index = l.index(v)
                    elif v == TYPE_LABEL:
                        type_index = l.index(v)
                l_index += 1
                continue
            
            try:
                if ipaddress.ip_address(l[addr_index]):
                    with_mapping.add(l[addr_index])
                    if type_index != -1:
                        mapper[l[addr_index]] = l[type_index]
            except ValueError:
                print(f"Invalid IP address: {l[addr_index]}")
                pass
    
    return mapping, with_mapping, mapper