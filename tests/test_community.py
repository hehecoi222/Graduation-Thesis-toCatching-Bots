import unittest
import os
import sys
import networkx as nx
from evaluate import return_mapping, get_scores

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from p2p_clustering.p2p_clustering import Clustering
from preprocess_data import preprocess_data
from graph_detect.graph_building import construct_graph
from graph_detect.evaluate_community import louvain_community_detection


class TestCommunityBuilding(unittest.TestCase):
    
    def get_bai_bsi(self, G, comm, mapping):        
        ip_com_mapping = {}
        
        for e_com in comm:
            hash_comm = hash(tuple(sorted(e_com)))
            for node in e_com:
                ip = G.nodes[node]['cls_def'][0]
                if ip not in ip_com_mapping:
                    ip_com_mapping[ip] = set()
                ip_com_mapping[ip].add(hash_comm)
                
        through = []
        a, b, c = 0, 0, 0
        for ip1 in ip_com_mapping:
            through.append(ip1)
            for ip2 in ip_com_mapping:
                if ip1 != ip2 and ip2 not in through:
                    try:
                        if mapping[ip1] == mapping[ip2]:
                            if len(ip_com_mapping[ip1].intersection(ip_com_mapping[ip2])) == 0:
                                b += 1
                            else:
                                a += 1
                        elif len(ip_com_mapping[ip1].intersection(ip_com_mapping[ip2])) != 0:
                            c += 1
                    except KeyError as e:
                        continue
        print(f"A: {a}, B: {b}, C: {c}")
        return a/(a+c), a/(a+b)
                        
    @classmethod
    def setUpClass(cls):
        preprocess_data.read_df_write_new('../../FullDS/out.csv', threshold_percent=10.0)
        cls.cluster = Clustering('out_file/new_infile.csv', local_subnet='163.194.0.0/16', dd_threshold=17, coverage_threshold=0.64)
        cls.cluster.run()
        cls.cluster.remove_same_hosting()
        _, _, cls.mapping = return_mapping('../../FullDS/out.csv', '../../FullDS/bot_mapping.txt')
        
    @classmethod
    def tearDownClass(cls):
        # This runs once after all tests
        cls.cluster.clean()
        
    def setUp(self):
        pass

    def tearDown(self):
        # Teardown fixture: runs after each test
        pass  # Clean up resources if needed

    def test_CommunityBuilding_0_01(self):
        # Test case for community building
        G = construct_graph(nx.Graph(), self.__class__.cluster.p2p_clusters, MCR_THRESHOLD=0.01)
        comm = louvain_community_detection(G)
        bsi, bai = self.get_bai_bsi(G, comm, self.__class__.mapping)
        print(f"BSI: {bsi}, BAI: {bai}")
        
    def test_CommunityBuilding_0_05(self):
        # Test case for community building
        G = construct_graph(nx.Graph(), self.__class__.cluster.p2p_clusters, MCR_THRESHOLD=0.05)
        comm = louvain_community_detection(G)
        bsi, bai = self.get_bai_bsi(G, comm, self.__class__.mapping)
        print(f"BSI: {bsi}, BAI: {bai}")
        
    def test_CommunityBuilding_0_1(self):
        # Test case for community building
        G = construct_graph(nx.Graph(), self.__class__.cluster.p2p_clusters, MCR_THRESHOLD=0.1)
        comm = louvain_community_detection(G)
        bsi, bai = self.get_bai_bsi(G, comm, self.__class__.mapping)
        print(f"BSI: {bsi}, BAI: {bai}")
        
    def test_CommunityBuilding_0_15(self):
        # Test case for community building
        G = construct_graph(nx.Graph(), self.__class__.cluster.p2p_clusters, MCR_THRESHOLD=0.15)
        comm = louvain_community_detection(G)
        bsi, bai = self.get_bai_bsi(G, comm, self.__class__.mapping)
        print(f"BSI: {bsi}, BAI: {bai}")
        

if __name__ == '__main__':
    unittest.main()