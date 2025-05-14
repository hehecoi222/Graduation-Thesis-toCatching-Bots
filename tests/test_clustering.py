import unittest
import os
import sys
from evaluate import return_mapping, get_scores

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from p2p_clustering.p2p_clustering import Clustering
from preprocess_data import preprocess_data


class TestClustering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        preprocess_data.read_df_write_new('../../FullDS/out.csv', threshold_percent=10.0)
        cls.mapping, cls.info_bots, _ = return_mapping('../../FullDS/out.csv', '../../FullDS/p2p.txt')

    def setUp(self):
        self.cluster = Clustering('out_file/new_infile.csv', local_subnet='163.194.0.0/16')
        

    def tearDown(self):
        # Teardown fixture: runs after each test
        self.cluster.clean()
        pass  # Clean up resources if needed

    def test_Clustering_DD_10(self):
        # Test case for DD threshold of 10
        self.cluster.dd_threshold = 10
        self.cluster.run()
        print(get_scores(self.__class__.mapping, self.__class__.info_bots, self.cluster.local_subnet, self.cluster.list_p2p))
        
    def test_Clustering_DD_20(self):
        # Test case for DD threshold of 20
        self.cluster.dd_threshold = 20
        self.cluster.run()
        print(get_scores(self.__class__.mapping, self.__class__.info_bots, self.cluster.local_subnet, self.cluster.list_p2p))
        
    def test_Clustering_DD_30(self):
        # Test case for DD threshold of 30
        self.cluster.dd_threshold = 30
        self.cluster.run()
        print(get_scores(self.__class__.mapping, self.__class__.info_bots, self.cluster.local_subnet, self.cluster.list_p2p))
        
    def test_Clustering_DD_50(self):
        # Test case for DD threshold of 50
        self.cluster.dd_threshold = 50
        self.cluster.run()
        print(get_scores(self.__class__.mapping, self.__class__.info_bots, self.cluster.local_subnet, self.cluster.list_p2p))

if __name__ == '__main__':
    unittest.main()