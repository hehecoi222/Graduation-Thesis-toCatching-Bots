from preprocess_data import preprocess_data
from p2p_clustering import p2p_clustering
from graph_detect import graph_building, evaluate_community
import networkx as nx

def all(file, threshold_percent=10.0, dd_threshold=10, coverage_threshold=0.5, local_subnet='0.0.0.0/32', MCR_THRESHOLD=0.1, AVG_DD_THRESHOLD=0.3, AVG_MCR_THRESHOLD=0.1, new_way=True):
    preprocess_data.read_df_write_new(file, threshold_percent=threshold_percent)
    cluster = p2p_clustering.Clustering('out_file/new_infile.csv', new_way=new_way, dd_threshold=dd_threshold, coverage_threshold=coverage_threshold, local_subnet=local_subnet)
    cluster.run()
    cluster.remove_same_hosting()
    
    print(len(cluster.p2p_clusters))
    G = graph_building.construct_graph(nx.Graph(), cluster.p2p_clusters, MCR_THRESHOLD=MCR_THRESHOLD)
    return evaluate_community.evaluate_community(G, new_way=new_way, AVG_DD_THRESHOLD=AVG_DD_THRESHOLD, AVG_MCR_THRESHOLD=AVG_MCR_THRESHOLD)
    
def main():
    print(all('../../FullDS/out.csv', threshold_percent=10.0, dd_threshold=17, coverage_threshold=0.65, local_subnet='163.194.0.0/16', MCR_THRESHOLD=0.095, AVG_DD_THRESHOLD=0.3, AVG_MCR_THRESHOLD=0.01, new_way=True))
    
if __name__ == "__main__":
    main()