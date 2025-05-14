from preprocess_data import preprocess_data
from p2p_clustering import p2p_clustering
from graph_detect import graph_building, evaluate_community

def all(file, threshold_percent=10.0, dd_threshold=10, coverage_threshold=0.5, local_subnet='0.0.0.0/32', MCR_THRESHOLD=0.1, AVG_DD_THRESHOLD=0.3, AVG_MCR_THRESHOLD=0.1, new_way=True):
    preprocess_data.read_df_write_new(file, threshold_percent=threshold_percent)
    cluster = p2p_clustering.Clustering('out_file/new_infile.csv', new_way=new_way, dd_threshold=dd_threshold, coverage_threshold=coverage_threshold, local_subnet=local_subnet)
    cluster.run()
    
    G = graph_building.construct_graph(cluster.p2p_clusters, MCR_THRESHOLD=MCR_THRESHOLD)
    return evaluate_community.evaluate_community(G, new_way=new_way, AVG_DD_THRESHOLD=AVG_DD_THRESHOLD, AVG_MCR_THRESHOLD=AVG_MCR_THRESHOLD)
    
def main():
    import os

    current_project_dir = os.path.dirname(os.path.abspath(__file__))
    print("Current project directory:", current_project_dir)
    
if __name__ == "__main__":
    main()