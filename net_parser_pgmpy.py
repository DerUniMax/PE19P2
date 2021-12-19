import pandas as pd
from edgesAndNodes import edges, nodes
from pgmpy.readwrite import BIF
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.estimators import MaximumLikelihoodEstimator

# df = pd.read_csv("P1_DP13_Wohnungen_X.csv", sep=";")

def parse(df: pd.DataFrame, edges: [tuple]):
  nodes = _extract_nodes(edges)
  
  net = BayesianNetwork(edges)

  estimator = BayesianEstimator(net, df)

  for node in nodes:
    print('Estimate: ', node)
    CPD = estimator.estimate_cpd(node, prior_type='BDeu')
    net.add_cpds(CPD)
    print(CPD)

  print('Saving xmlbif')

  net.save("net.xml", filetype='xmlbif')

  print('Saved xmlbif')

  return net

def _extract_nodes(edges: [tuple]) -> [str]:
  def is_in_list(list: [], search_item) -> bool:
    for item in list:
      if search_item == item:
        return True
    return False
  
  node_list = []
  
  for edge in edges:
    if not is_in_list(node_list, edge[0]):
      node_list.append(edge[0])
    
    if not is_in_list(node_list, edge[1]):
      node_list.append(edge[1])
  
  return node_list