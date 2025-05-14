import re
from p2p_clustering import file_handling
import ipaddress
import ipinfo_db

client = ipinfo_db.Client('')

class Clustering:
    def __init__(self, file, new_way=True, dd_threshold=10, coverage_threshold=0.5, local_subnet='0.0.0.0/32'):
        self.file = file
        self.new_way = new_way
        self.cluster = {}
        self.p2p_clusters = {}
        self.list_p2p = set()
        self.len_cluster = 0
        self.num_clusters = 0
        self.dd_threshold = dd_threshold
        self.coverage_threshold = coverage_threshold
        self.local_subnet = local_subnet
        
    def remove_same_hosting(self):
        global p2p_clusters
        # Iterate through p2p clusters
        map_ip = {}
        coverage = {}
        remove_set = set()
        for flow_guid, cluster in self.p2p_clusters.items():
            # Get the list of flows
            flows = cluster['list_flows']
            
            # Iterate through each flow
            for flow in flows:
                # Ignore local IPs
                if ipaddress.ip_address(flow[0]) not in ipaddress.ip_network(self.local_subnet, strict=False):
                    asn = client.getASN(flow[0])
                    map_ip[flow[0]] = asn
                    if asn not in coverage:
                        coverage[asn] = set()
                    coverage[asn].add(cluster['cls_def'][0])

        # Re-iterate through p2p clusters to remove local IPs, also IP high coverage
        for flow_guid, cluster in self.p2p_clusters.items():
            # Get the list of flows
            flows = cluster['list_flows']

            new_flows = []
            new_dd_set = set()
            
            # Iterate through each flow
            for flow in flows:
                # Get IP ASN
                asn = map_ip.get(flow[0])
                # Check coverage
                if asn is not None and len(coverage[asn])/len(self.list_p2p) >= self.coverage_threshold:
                    remove_set.add(flow[0])
                    continue
                new_flows.append(flow)
                # new_dd_set.add(ipaddress.ip_network(flow[0]+'/16', strict= False).network_address)
                new_dd_set.add(client.getASN(flow[0]))
            # Update the cluster with the new flows
            cluster['list_flows'] = new_flows
            # Update the DDI count
            cluster['dd_set'] = new_dd_set
            cluster['ddi'] = len(new_dd_set)

    def run(self):
        with open(self.file) as f:
            l_index = 0
            for line in f:
                # If first line (header)
                if (l_index == 0):
                    src_index, dst_index, proto_index, bpp_in_index, bpp_out_index, g_bpp_in_index, g_bpp_out_index = file_handling.define_index(line)
                    l_index += 1
                    continue
                
                # Split line into list
                l = re.split(r',|\n|\t', line)
                
                # Keep flow TCP and UDP only
                if (l[proto_index] != '6') and (l[proto_index] != '17'):
                    continue
                
                temp_key = ()
                if self.new_way:
                    temp_key = (l[src_index], l[proto_index], int(l[g_bpp_out_index]), int(l[g_bpp_in_index]),)
                else:
                    temp_key = (l[src_index], l[proto_index], int(l[bpp_out_index]), int(l[bpp_in_index]),)
                
                # Generate GUID for flow
                flow_guid = hash(temp_key).__str__()

                temp_cluster = self.cluster
                cluster_filenum = -1
                
                # Add to cluster
                if flow_guid not in self.cluster:
                    temp_cluster,cluster_filenum = file_handling.find_cluster(flow_guid, self.num_clusters)
                    if cluster_filenum == -1:
                        temp_cluster = self.cluster
                        temp_cluster[flow_guid] = dict(cls_def=temp_key, ddi=0, dd_set = set(), list_flows=[(l[dst_index],)])
                        self.len_cluster += 1
                else:
                    temp_cluster[flow_guid]['list_flows'].append((l[dst_index],))
                    
                # Update DDI count
                if self.new_way:
                    temp_cluster[flow_guid]['dd_set'].add(client.getASN(l[dst_index]))
                else:
                    temp_cluster[flow_guid]['dd_set'].add(ipaddress.ip_network(l[dst_index]+'/16', strict= False).network_address)
                temp_cluster[flow_guid]['ddi'] = len(temp_cluster[flow_guid]['dd_set'])
                
                # Check if DDI meet threshold, then it is P2P
                if temp_cluster[flow_guid]['ddi'] >= self.dd_threshold:
                    self.p2p_clusters[flow_guid] = temp_cluster[flow_guid]
                    self.list_p2p.add(l[src_index])

                # Check if there is read outside of cluster
                if cluster_filenum != -1:
                    file_handling.save_cluster(temp_cluster, cluster_filenum)

                # Dump cluster to file
                if self.len_cluster % 2000000 == 0 and cluster_filenum == -1:
                    file_handling.save_cluster(self.cluster, self.num_clusters)
                    self.cluster = {}
                    self.num_clusters += 1
                    print("Dumped clusters: ", self.num_clusters)
                
                # Increment line index
                l_index += 1
                if l_index % 500000 == 0:
                    print("Processed: ", l_index)
                    
        self.remove_same_hosting()