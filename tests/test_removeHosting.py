import ipaddress
import unittest
import os
import sys
from evaluate import return_mapping, get_scores

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from p2p_clustering.p2p_clustering import Clustering
from preprocess_data import preprocess_data


class TestRemoveHosting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        preprocess_data.read_df_write_new('../../FullDS/out.csv', threshold_percent=10.0)
        cls.cluster = Clustering('out_file/new_infile.csv', local_subnet='163.194.0.0/16', dd_threshold=17)
        cls.cluster.run()
        cls.mapping = set()
        for flow_guid, cluster in cls.cluster.p2p_clusters.items():
            # Get the list of flows
            flows = cluster['list_flows']
            
            # Iterate through each flow
            for flow in flows:
                # Ignore local IPs
                if ipaddress.ip_address(flow[0]) not in ipaddress.ip_network('163.194.0.0/16', strict=False):
                    cls.mapping.add(flow[0])
                    

    def setUp(self):
        self.cluster = Clustering('out_file/new_infile.csv', local_subnet='163.194.0.0/16', dd_threshold=17)
        self.cluster.run()

    def tearDown(self):
        # Teardown fixture: runs after each test
        self.cluster.clean()
        pass  # Clean up resources if needed

    def test_RemoveHosting_0_5(self):
        self.cluster.coverage_threshold = 0.5
        remove_set = self.cluster.remove_same_hosting()
        print(f"Remove total: {len(remove_set)}, percentage: {len(remove_set) / len(self.__class__.mapping) * 100:.2f}%, with remove wrong: {len(remove_set.intersection(self.cluster.list_p2p))}")
        
    def test_RemoveHosting_0_6(self):
        self.cluster.coverage_threshold = 0.6
        remove_set = self.cluster.remove_same_hosting()
        print(f"Remove total: {len(remove_set)}, percentage: {len(remove_set) / len(self.__class__.mapping) * 100:.2f}%, with remove wrong: {len(remove_set.intersection(self.cluster.list_p2p))}")
        
    def test_RemoveHosting_0_7(self):
        self.cluster.coverage_threshold = 0.7
        remove_set = self.cluster.remove_same_hosting()
        print(f"Remove total: {len(remove_set)}, percentage: {len(remove_set) / len(self.__class__.mapping) * 100:.2f}%, with remove wrong: {len(remove_set.intersection(self.cluster.list_p2p))}")
        
    def test_RemoveHosting_0_8(self):
        self.cluster.coverage_threshold = 0.8
        remove_set = self.cluster.remove_same_hosting()
        print(f"Remove total: {len(remove_set)}, percentage: {len(remove_set) / len(self.__class__.mapping) * 100:.2f}%, with remove wrong: {len(remove_set.intersection(self.cluster.list_p2p))}")
        
    def test_RemoveHosting_0_9(self):
        self.cluster.coverage_threshold = 0.9
        remove_set = self.cluster.remove_same_hosting()
        print(f"Remove total: {len(remove_set)}, percentage: {len(remove_set) / len(self.__class__.mapping) * 100:.2f}%, with remove wrong: {len(remove_set.intersection(self.cluster.list_p2p))}")

if __name__ == '__main__':
    unittest.main()