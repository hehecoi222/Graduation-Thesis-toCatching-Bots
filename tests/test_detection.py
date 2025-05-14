import unittest
import os
import sys
import networkx as nx
from evaluate import return_mapping, get_scores

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from p2p_clustering.p2p_clustering import Clustering
from preprocess_data import preprocess_data
from graph_detect.graph_building import construct_graph
from graph_detect.evaluate_community import evaluate_community


class TestDetection(unittest.TestCase):
                        
    @classmethod
    def setUpClass(cls):
        preprocess_data.read_df_write_new('../../FullDS/out.csv', threshold_percent=10.0)
        cls.cluster = Clustering('out_file/new_infile.csv', local_subnet='163.194.0.0/16', dd_threshold=20, coverage_threshold=0.6)
        cls.cluster.run()
        cls.cluster.remove_same_hosting()
        cls.Graph = construct_graph(nx.Graph(), cls.cluster.p2p_clusters, MCR_THRESHOLD=0.02)
        cls.mapping, cls.bot_mapping,_ = return_mapping('../../FullDS/out.csv', '../../FullDS/bot_mapping.txt')
        
    @classmethod
    def tearDownClass(cls):
        # This runs once after all tests
        cls.cluster.clean()
        
    def setUp(self):
        pass

    def tearDown(self):
        # Teardown fixture: runs after each test
        pass  # Clean up resources if needed
    
    def test_Detection_DD0_01_MCR0_01(self):
        list_bots = evaluate_community(self.__class__.Graph, new_way=True, AVG_DD_THRESHOLD=0.01, AVG_MCR_THRESHOLD=0.01)
        print(get_scores(self.__class__.mapping, self.__class__.bot_mapping, self.__class__.cluster.local_subnet, list_bots))
        
    def test_Detection_DD0_01_MCR0_1(self):
        list_bots = evaluate_community(self.__class__.Graph, new_way=True, AVG_DD_THRESHOLD=0.01, AVG_MCR_THRESHOLD=0.1)
        print(get_scores(self.__class__.mapping, self.__class__.bot_mapping, self.__class__.cluster.local_subnet, list_bots))
        
    def test_Detection_DD0_01_MCR0_005(self):
        list_bots = evaluate_community(self.__class__.Graph, new_way=True, AVG_DD_THRESHOLD=0.01, AVG_MCR_THRESHOLD=0.005)
        print(get_scores(self.__class__.mapping, self.__class__.bot_mapping, self.__class__.cluster.local_subnet, list_bots))
        
    def test_Detection_DD0_01_MCR0_05(self):
        list_bots = evaluate_community(self.__class__.Graph, new_way=True, AVG_DD_THRESHOLD=0.01, AVG_MCR_THRESHOLD=0.05)
        print(get_scores(self.__class__.mapping, self.__class__.bot_mapping, self.__class__.cluster.local_subnet, list_bots))
        
    def test_Detection_DD0_8_MCR0_07(self):
        list_bots = evaluate_community(self.__class__.Graph, new_way=True, AVG_DD_THRESHOLD=0.8, AVG_MCR_THRESHOLD=0.07)
        print(get_scores(self.__class__.mapping, self.__class__.bot_mapping, self.__class__.cluster.local_subnet, list_bots))

if __name__ == '__main__':
    unittest.main()