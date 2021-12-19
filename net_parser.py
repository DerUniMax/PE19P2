import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.factors.discrete import TabularCPD
import json

def parse(df: pd.DataFrame, edges: [tuple], save_file: str):
  nodes = _extract_nodes(edges)
  
  net = BayesianNetwork(edges)

  estimator = BayesianEstimator(net, df)

  for node in nodes:
    print('Estimate: ', node)
    CPD = estimator.estimate_cpd(node, prior_type='BDeu')
    net.add_cpds(CPD)
    print(CPD)

  _export_as_json(net, save_file)

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

def _export_as_json(net: BayesianNetwork, filename: str):
  save_obj = dict()
  
  save_obj['name'] = net.name
  
  save_obj['nodes'] = list(net.nodes)
  
  save_obj['edges'] = list(net.edges)
  
  save_obj['cpds'] = list([_format_cpd(cpd) for cpd in net.cpds])
  
  with open(filename, 'w') as file:
    json.dump(save_obj, file)

def _format_cpd(cpd: TabularCPD):
  ret_cpd = dict()
  
  ret_cpd['values'] = cpd.get_values().tolist()
  
  ret_cpd['variable'] = cpd.variable
  
  ret_cpd['variable_card'] = cpd.variable_card
  
  ret_cpd['evidence'] = cpd.variables[1:]
  
  ret_cpd['state_names'] = cpd.state_names
  
  return ret_cpd